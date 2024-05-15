"""
Initialization of the IDUN Guardian Client
"""

import os
import asyncio
from typing import Union
import logging
from .constants import LOG_FORMAT
from .guardian_ble import GuardianBLE
from .guardian_recording import GuardianRecording, Subscription
from .guardian_http_api import GuardianHttpAPI
from .utils import check_ble_address
from .types import FileTypes
from typing import Union
from bleak import exc
from .exceptions import APIRequestError
from .polling_service import PollingService

from .event_handlers import (
    LiveInsightsEvent,
    RealtimePredictionEvent,
    default_console_handler,
)

logger = logging.getLogger("idun_guardian_sdk")


class GuardianClient:
    """
    Class object for the communication between Guardian Earbuds and Cloud API
    """

    _ws_endpoint_url = "wss://wpcg36nil5.execute-api.eu-central-1.amazonaws.com/v1/"
    _http_endpoint_url = "https://d3pq71txhb.execute-api.eu-central-1.amazonaws.com/"

    def __init__(
        self,
        address: Union[str, None] = None,
        ws_endpoint_url=None,
        http_endpoint_url=None,
        api_token: Union[str, None] = None,
        debug=False,
    ) -> None:
        """Initialize the Guardian Client

        Args:
            address (str, optional): The MAC address of the Guardian Earbuds. Defaults to "00000000-0000-0000-0000-000000000000".

        Raises:
            ValueError: If the MAC address is not valid
        """
        self.is_connected = False
        self.ble_connection_status = 0
        self._polling_service = PollingService()
        self._configure_logger(debug)
        self.address = address
        self._api_token = api_token
        self._guardian_ble = None
        self._guardian_http_api = None
        self._guardian_recording = None

        if ws_endpoint_url is not None:
            self._ws_endpoint_url = ws_endpoint_url

        if http_endpoint_url is not None:
            self._http_endpoint_url = http_endpoint_url

    @property
    def api_token(self):
        # If not provided during initialization, check the environment variable
        if not self._api_token:
            self._api_token = os.environ.get("IDUN_API_TOKEN")

        if self._api_token is None:
            raise ValueError("API token is not provided. Please provide an API token.")

        return self._api_token

    @property
    def guardian_ble(self):
        if self._guardian_ble is None:
            if self.address is not None:
                if check_ble_address(self.address):
                    self._guardian_ble = GuardianBLE(self.address)
            else:
                self._guardian_ble = GuardianBLE()
        return self._guardian_ble

    @property
    def guardian_http_api(self):
        if self._guardian_http_api is None:
            self._guardian_http_api = GuardianHttpAPI(self._http_endpoint_url, self.api_token)
        return self._guardian_http_api

    @property
    def guardian_recording(self):
        if self._guardian_recording is None:
            self._guardian_recording = GuardianRecording(
                ws_url=self._ws_endpoint_url, api_token=self.api_token
            )
        return self._guardian_recording

    def _configure_logger(self, debug):
        """Configure the logger for the Guardian Client"""
        log_level = logging.DEBUG if debug else logging.INFO
        logger.propagate = False

        formatter = logging.Formatter(LOG_FORMAT)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(log_level)

        logger.setLevel(log_level)
        logger.addHandler(stream_handler)

    def get_recording_id(self):
        if not self.guardian_recording.recording_id:
            raise ValueError("Recording ID is not yet available. Recording is not started.")
        return self.guardian_recording.recording_id

    # ------------------ BLE section ------------------
    async def search_device(self):
        """Connect to the Guardian Earbuds

        Returns:
            is_connected: bool
        """

        self.address = await self.guardian_ble.search_device()

        return self.address

    async def get_device_address(self) -> str:
        """Get the MAC address of the Guardian Earbuds.
        It searches the MAC address of the device automatically. This
        address is used as the deviceID for cloud communication
        """
        device_address = await self.guardian_ble.get_device_mac(self.guardian_ble.client)
        return device_address

    async def check_battery(self):
        """
        Start recording data from the Guardian Earbuds.
        Unidirectional websocket connection to the Guardian Cloud API.
        """
        ble_client_task = asyncio.create_task(self.guardian_ble.read_battery_level())
        await asyncio.wait([ble_client_task])

    async def stream_impedance(self, mains_freq_60hz, handler=None):
        """
        Args:
            mains_freq_60hz (bool, optional): Set to True if the mains frequency is 60Hz. Defaults to False.
            handler: The callback function to handle the impedance data
        """
        await self.guardian_ble.stream_impedance(mains_freq_60hz=mains_freq_60hz, handler=handler)

    # ------------------ Live Recording section ------------------
    def subscribe_live_insights(
        self, raw_eeg=False, filtered_eeg=False, imu=False, handler=default_console_handler
    ):
        stream_types = []
        if raw_eeg:
            stream_types.append("RAW_EEG")
        if filtered_eeg:
            stream_types.append("FILTERED_EEG")
        if imu:
            stream_types.append("IMU")

        if len(stream_types) == 0:
            raise ValueError(
                "At least one stream type must be selected: raw_eeg=True | fileterd_eeg=True | imu=True"
            )

        self.guardian_recording.msg_handler.subscribe(LiveInsightsEvent, handler)
        subs = Subscription(identifiers=stream_types, event_type=LiveInsightsEvent)
        self.guardian_recording.ws_subscriptions.append(subs)

    def subscribe_realtime_predictions(
        self, fft=False, jaw_clench=False, bin_heog=False, handler=default_console_handler
    ):
        predictions = []
        if fft:
            predictions.append("FFT")
        if jaw_clench:
            predictions.append("JAW_CLENCH")
        if bin_heog:
            predictions.append("BIN_HEOG")

        if len(predictions) == 0:
            raise ValueError(
                "At least one stream type must be selected: fft=True | jaw_clench=True | bin_heog=True"
            )

        self.guardian_recording.msg_handler.subscribe(RealtimePredictionEvent, handler)
        subs = Subscription(identifiers=predictions, event_type=RealtimePredictionEvent)
        self.guardian_recording.ws_subscriptions.append(subs)

    async def start_recording(
        self,
        recording_timer: int = 36000,
        led_sleep: bool = False,
    ):
        """
        Start recording data from the Guardian Earbuds.
        Unidirectional websocket connection to the Guardian Cloud API.

        Args:
            recording_timer (int, optional): The duration of the recording in seconds. Defaults to 36000.
            led_sleep (bool, optional): Enable LED sleep mode. Defaults to False.

        Raises:
            ValueError: If the recording timer is not valid
        """
        self._end_ongoing_recordings()
        try:
            logger.info("[CLIENT]: Starting recording")
            logger.info(f"[CLIENT]: Recording timer: {recording_timer} seconds")

            data_queue: asyncio.Queue = asyncio.Queue(maxsize=86400)

            while self.ble_connection_status == 0:  # TRUE FALSE
                self.ble_connection_status = await self.guardian_ble.connect_to_device()
                logger.debug(f"[CLIENT]: Current Device BLE Status={self.ble_connection_status}")

            self.guardian_recording.device_id = self.guardian_ble.mac_id

            logger.debug("[CLIENT]: Validating if API Device ID matches with BLE Device ID")
            api_device_id = self.get_user_info().get("device_id")
            if not api_device_id:
                raise ValueError("Failed to get Device ID from the API")
            if api_device_id != self.guardian_recording.device_id:
                raise ValueError(
                    f"API device ID {api_device_id} does not match with BLE device ID {self.guardian_recording.device_id}"
                )
            else:
                logger.debug(
                    "[CLIENT]: Validation passed: API Device ID matches with BLE Device ID"
                )

            task_list = []
            task_list.append(
                asyncio.create_task(
                    self.guardian_ble.run_ble_record(
                        self.guardian_recording,
                        data_queue,
                        recording_timer,
                        led_sleep,
                    )
                )
            )
            task_list.append(
                asyncio.create_task(
                    self.guardian_recording.start_streaming(
                        data_queue,
                    )
                )
            )

            await asyncio.gather(*task_list)

        except exc.BleakError as err:
            logger.error("[CLIENT]: BLE error: %s", err)
        except asyncio.exceptions.CancelledError:
            logger.debug("Keyboard interrupt received, terminating tasks")
        logger.info("[CLIENT] Recording Finished")
        logger.debug("[CLIENT]: -----------  All tasks are COMPLETED -----------")
        logger.info(f"[CLIENT]: Recording ID {self.guardian_recording.recording_id}")

        return self.guardian_recording.recording_id

    # ------------------ HTTP API section ------------------
    def download_file(self, recording_id: str, file_type: FileTypes, file_path: str = None):
        """
        Download a file from a recording. Possible file types are: EEG, IMU, IMPEDANCE
        :param recording_id: the id of the recording
        :param file_type: the type of file to download
        :param file_path: where to save the file
        """
        url = self.guardian_http_api.download_recording(
            recording_id=recording_id, file_type=file_type
        )
        self.guardian_http_api.save_file_from_s3(url, file_path)

    def get_recordings(self, limit=200, status=None, page_index=None):
        return self.guardian_http_api.get_recordings(limit, status, page_index)

    def delete_recording(self, recording_id):
        return self.guardian_http_api.delete_recording(recording_id)

    def end_recording(self, recording_id):
        return self.guardian_http_api.end_recording(recording_id)

    def update_recording_tags(self, recording_id, tags):
        return self.guardian_http_api.update_recording_tags(recording_id, tags)

    def update_recording_display_name(self, recording_id, display_name):
        return self.guardian_http_api.update_recording_display_name(recording_id, display_name)

    def generate_and_download_sleep_report(self, recording_id, file_path=None):
        self.guardian_http_api.generate_sleep_report(recording_id)
        try:
            logger.info("Waiting for the report to be ready...")
            url = self._polling_service.poll_until_ready(
                self.guardian_http_api.download_sleep_report, recording_id=recording_id
            )
        except Exception as e:
            raise APIRequestError(
                f"Failed to generate sleep report for recording {recording_id}. {str(e)}"
            )

        saved_path = self.guardian_http_api.save_file_from_s3(url, file_path)
        logger.info(f"Sleep report downloaded successfully at: {saved_path}")

    def generate_and_download_daytime_report(self, recording_id, file_path=None):
        self.guardian_http_api.generate_daytime_report(recording_id)
        logger.info("Waiting for the report to be ready...")
        try:
            url = self._polling_service.poll_until_ready(
                self.guardian_http_api.download_daytime_report, recording_id=recording_id
            )
        except Exception as e:
            raise APIRequestError(
                f"Failed to generate daytime report for recording {recording_id}. {str(e)}"
            )

        saved_path = self.guardian_http_api.save_file_from_s3(url, file_path)
        logger.info(f"Daytime report downloaded successfully at: {saved_path}")

    def get_user_info(self):
        return self.guardian_http_api.get_user_info()

    def _end_ongoing_recordings(self):
        """
        Get recordings with status ONGOING and NOT_STARTED and end them
        """
        logger.debug("[CLIENT]: Ending ongoing recordings if any")
        recs = []
        recs.extend(self.get_recordings(status="ONGOING").get("items", []))
        recs.extend(self.get_recordings(status="NOT_STARTED").get("items", []))

        for rec in recs:
            self.end_recording(rec["recordingId"])
