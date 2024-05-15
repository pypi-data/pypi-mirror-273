"""
Guardian API websocket utilities.
"""

import base64
from collections import namedtuple
import json
import socket
import time
import asyncio
import websockets
import time
from typing import Optional

from .debug_logs import *
from .utils import exit_system

from .event_handlers import (
    LiveInsightsEvent,
    RealtimePredictionEvent,
    RecordingUpdateEvent,
    ClientError,
    default_console_handler,
)
from .utils import now
from .websocket_messages import (
    StartNewRecording,
    SubscribeLiveStreamInsights,
    SubscribeRealtimePredictions,
    EndOngoingRecording,
)
from .ws_msg_handler import WsMsgHandler

Subscription = namedtuple("Subscription", ["identifiers", "event_type"])

logger = logging.getLogger("idun_guardian_sdk")


class GuardianRecording:
    """Main Guardian API client."""

    def __init__(self, ws_url: str, api_token: str) -> None:
        """Initialize Guardian API client.

        Args:
            debug (bool, optional): Enable debug logging. Defaults to True.
        """
        self.ping_timeout: int = 2
        self.retry_time: int = 2
        self.sample_rate = 250
        self.sentinal = object()
        self.initial_receipt_timeout = 15
        self.receipt_timeout = self.initial_receipt_timeout
        self.sending_time_limit = 0.01
        self.bi_directional_timeout = 15
        self.last_saved_time = time.time()
        self.connected = False
        self.data_to_send = {}
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None  # type: ignore
        self.api_token = api_token
        self.device_id = ""
        self.recording_id = ""
        self.password = ""
        self.rec_started = False
        self.rec_ended = False
        self.ws_url = ws_url
        self.api_token = api_token
        self.ws_url_auth = f"{self.ws_url}?authorization={self.api_token}"
        self.ws_subscriptions = []
        self.ws_subscriptions_done = False
        self.msg_handler = WsMsgHandler()
        self._subscribe_internal_msg_handlers()

    def _subscribe_internal_msg_handlers(self):
        self.msg_handler.subscribe(ClientError, default_console_handler)
        self.msg_handler.subscribe(RecordingUpdateEvent, self._handle_recording_update)

    def _handle_recording_update(self, event: RecordingUpdateEvent):
        status = event.message.get("status", None)
        if status in ["COMPLETED", "FAILED"]:
            self.rec_ended = True
            logger.debug("[API]: Final receit got! Ending receive messages")
        elif status == "NOT_STARTED":
            logger.debug(f"[API]: Setting recording_id: {event.message.get('recordingId')}")
            self.recording_id = event.message.get("recordingId")
            self.rec_started = True
        elif status == "PROCESSING":
            # Do something?
            pass
        elif status == "ONGOING":
            # Do something?
            pass
        else:
            logger.warning(f"[API]: Unexpected recording update status: {status}.")

    async def start_streaming(
        self,
        data_queue: asyncio.Queue,
    ) -> None:
        """Connect to the Guardian API websocket.

        Args:
            data_queue (asyncio.Queue): Data queue from the BLE client

        Raises:
            Exception: If the websocket connection fails
        """

        async def send_start_recording():
            msg = StartNewRecording(deviceId=self.device_id, deviceTs=now()).to_dict()
            if not data_queue.full():
                await asyncio.shield(data_queue.put(msg))
            else:
                await asyncio.shield(data_queue.get())
                await asyncio.shield(data_queue.put(msg))

        async def wait_recording_end():
            while True:
                if self.rec_ended:
                    break
                logger.debug("[API]: Waiting recording end message from the server...")
                await asyncio.sleep(1)

        async def load_data_to_send():
            data_valid = False
            self.data_to_send = None
            package = await data_queue.get()
            # TODO: Add more data validation or just always trust the data queue
            self.data_to_send = package
            data_valid = bool(self.data_to_send)

            return data_valid

        async def handle_api_subscriptions():
            while not self.ws_subscriptions_done:
                await asyncio.sleep(0.5)
                if self.connected and self.rec_started:
                    logger.debug("[API]: Started checking API subscrpitions!")
                    for subscription in self.ws_subscriptions:
                        logger.debug(f"[API]: Handling subscription: {subscription}")
                        msg = {}
                        if subscription.event_type == LiveInsightsEvent:
                            msg = SubscribeLiveStreamInsights(
                                deviceId=self.device_id,
                                recordingId=self.recording_id,
                                streamsTypes=subscription.identifiers,
                                deviceTs=now(),
                            ).to_dict()

                        if subscription.event_type == RealtimePredictionEvent:
                            msg = SubscribeRealtimePredictions(
                                deviceId=self.device_id,
                                recordingId=self.recording_id,
                                predictions=subscription.identifiers,
                                deviceTs=now(),
                            ).to_dict()

                        if not msg:
                            # Shouldn't happen
                            raise ValueError("Invalid subscription event type")

                        if not data_queue.full():
                            await asyncio.shield(data_queue.put(msg))
                        else:
                            await asyncio.shield(data_queue.get())
                            await asyncio.shield(data_queue.put(msg))

                    self.ws_subscriptions_done = True
                    logger.debug("[API]: Subscriptions messages sent to Data Queue!")
            logger.debug("[API]: Handle subscriptions task finished")

        async def send_messages():
            while True:
                if not self.connected or self.rec_ended:
                    break
                if await load_data_to_send():
                    if self.data_to_send.get("STOP_SIGNAL"):
                        logger.debug(
                            "[API]: Received Stop Signal in Data Queue, stopping send_messages task"
                        )
                        break
                    await asyncio.shield(
                        asyncio.sleep(self.sending_time_limit)
                    )  # Wait as to not overload the cloud
                    await asyncio.shield(self.websocket.send(json.dumps(self.data_to_send)))

                if self.data_to_send.get("action") == "endOngoingRecording":
                    logging_stop_send()
                    self.receipt_timeout = 1000  # Wait until necessary for the stop to be sent
                    try:
                        await asyncio.wait_for(wait_recording_end(), timeout=30)
                        logger.debug("[API]: The Recording has been correctly stopped")
                    except Exception as e:
                        logger.debug(
                            f"[API]: We could not stop the recording, we will retry to fix the problem. \n Error: {e}"
                        )
                    break

        async def receive_messages():
            self.last_saved_time = time.time()
            while True:
                if not self.connected or self.rec_ended:
                    break

                message_str = await asyncio.shield(
                    asyncio.wait_for(self.websocket.recv(), timeout=self.receipt_timeout)
                )
                self.last_saved_time = time.time()
                if not message_str:
                    continue

                try:
                    event = {}
                    decoded = base64.b64decode(message_str).decode("utf-8")
                    event = json.loads(decoded)
                except Exception as e:
                    logger.error("Error Decoding received message:", e)
                    logger.debug("message_str:", message_str)
                    logger.debug("decoded:", decoded)
                    logger.debug("event:", event)

                action = event.get("action")
                if action is None:
                    logger.warning("[API]: Event without action will be discarded:", event)
                    continue
                if action == "liveStreamInsights":
                    self.msg_handler.publish(LiveInsightsEvent(event))
                elif action == "realtimePredictionsResponse":
                    self.msg_handler.publish(RealtimePredictionEvent(event))
                elif action == "recordingUpdate":
                    self.msg_handler.publish(RecordingUpdateEvent(event))
                elif action == "clientError":
                    self.msg_handler.publish(ClientError(event))
                    raise Exception("Websocket Client Error:", event.get("message"))
                else:
                    logger.warning(f"[API]: Unhandled action: {action}. Message: {event}")

                if self.rec_ended:
                    logger.debug(
                        "[API]: Adding Stop Signal in data_queue for send_messages task to end"
                    )
                    stop_signal = {"STOP_SIGNAL": True}
                    if not data_queue.full():
                        await asyncio.shield(data_queue.put(stop_signal))
                    else:
                        await asyncio.shield(data_queue.get())
                        await asyncio.shield(data_queue.put(stop_signal))
                    break
                bi_directional_timeout()

        def bi_directional_timeout():
            time_without_data = time.time() - self.last_saved_time
            if time_without_data > self.bi_directional_timeout:
                raise asyncio.TimeoutError("Bidirection timeout error")

        def on_connection_initialise_variables():
            self.connected = True
            self.receipt_timeout = self.initial_receipt_timeout

        async def handle_cancelled_error():
            logger.debug("Handling cancelled error")
            self.rec_ended = True
            async with websockets.connect(self.ws_url_auth) as self.websocket:
                self.data_to_send = EndOngoingRecording(
                    self.device_id, self.recording_id, now()
                ).to_dict()
                await self.websocket.send(json.dumps(self.data_to_send))
                await asyncio.sleep(0.1)
            return

        while True:
            logging_connecting_to_cloud()
            try:
                async with websockets.connect(self.ws_url_auth) as self.websocket:  # type: ignore
                    if not self.rec_started:
                        try:
                            log_sending_start_rec_info()
                            await send_start_recording()
                        except Exception:
                            exit_system()
                    try:
                        on_connection_initialise_variables()
                        # for the websocket we want to increase to initial timeout each time
                        logging_connection(self.ws_url)
                        send_task = asyncio.create_task(send_messages())
                        receive_task = asyncio.create_task(receive_messages())
                        handle_subs_task = asyncio.create_task(handle_api_subscriptions())
                        task_list = [send_task, receive_task]
                        if not self.ws_subscriptions_done:
                            task_list.append(handle_subs_task)
                        await asyncio.gather(*task_list)

                    except (websockets.exceptions.ConnectionClosed,) as error:  # type: ignore
                        try:
                            logging_connection_closed()
                            self.connected = False
                            await asyncio.shield(asyncio.sleep(self.ping_timeout))
                            logging_reconnection()
                            continue
                        except asyncio.CancelledError:
                            await handle_cancelled_error()

                    except asyncio.TimeoutError as error:
                        try:
                            log_interrupt_error(error)
                            self.connected = False
                            await asyncio.shield(asyncio.sleep(self.ping_timeout))
                            logging_reconnection()
                            continue
                        except asyncio.CancelledError:
                            await handle_cancelled_error()

                    except asyncio.CancelledError:
                        await handle_cancelled_error()

                    finally:
                        # Otherwise new tasks will be created which is a problem
                        try:
                            if not send_task.done():
                                send_task.cancel()
                            if not receive_task.done():
                                receive_task.cancel()
                        except Exception as error:
                            logger.debug("These tasks does not exist yet")

            except socket.gaierror as error:
                logging_gaieerror(error, self.retry_time)
                await asyncio.sleep(self.retry_time)
                continue

            except ConnectionRefusedError as error:
                logging_connection_refused(error, self.retry_time)
                await asyncio.sleep(self.retry_time)
                continue

            except Exception as error:
                log_interrupt_error(error)

            finally:
                # Otherwise new tasks will be created which is a problem
                try:
                    if not send_task.done():
                        send_task.cancel()
                    if not receive_task.done():
                        receive_task.cancel()
                except Exception as error:
                    logger.debug("These tasks does not exist yet")

            if self.rec_ended:
                logging_break()
                break

        logging_api_completed()
