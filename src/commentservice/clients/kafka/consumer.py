import logging
import threading
from collections.abc import Callable
from typing import Any

from confluent_kafka import (
    Consumer,
    KafkaError,
    KafkaException,
)

from commentservice.grpc import moderation_pb2

from .config import KafkaConfig

logger = logging.getLogger(__name__)

ModerationCallback = Callable[
    [moderation_pb2.ModerateObjectResponse, int], None
]


class ModerationResponseConsumer:
    def __init__(
        self, config: KafkaConfig, callback: ModerationCallback | None
    ) -> None:

        self.config = config
        self.callback = callback
        self.consumer = Consumer(config.get_consumer_config())
        self.topic = config.result_topic
        self.running: bool = False
        self.consumer_thread: threading.Thread | None = None

        self.consumer.subscribe([self.topic])
        logger.info(
            f"ModerationResponseConsumer subscribed to topic: {self.topic}"
        )

    def start(self) -> None:

        if self.running:
            logger.warning("Consumer already running")
            return

        self.running = True
        self.consumer_thread = threading.Thread(
            target=self._consume_loop, daemon=True
        )
        self.consumer_thread.start()
        logger.info("ModerationResponseConsumer started")

    def stop(self) -> None:

        if not self.running:
            return

        self.running = False

        if self.consumer_thread and self.consumer_thread.is_alive():
            self.consumer_thread.join(timeout=5.0)

        self.consumer.close()
        logger.info("ModerationResponseConsumer stopped")

    def _consume_loop(self) -> None:

        logger.info("Consumer loop started")

        while self.running:
            try:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                error = msg.error()
                if error is not None:
                    if error.code() == KafkaError._PARTITION_EOF:
                        logger.debug(
                            f"Reached end of partition for topic {msg.topic()}"
                        )
                    elif error.code() == KafkaError._TIMED_OUT:
                        logger.debug("Timeout")
                    else:
                        logger.error(f"Consumer error: {error}")
                    continue

                self._process_message(msg)

            except KafkaException as e:
                logger.error(f"Kafka exception in consume loop: {e}")
            except Exception as e:
                logger.error(f"Unexpected error in consume loop: {e}")

        logger.info("Consumer loop ended")

    def _process_message(self, msg: Any) -> None:

        try:
            request_id = 0
            if msg.key() is not None:
                try:
                    key_str = msg.key().decode("utf-8")
                    request_id = int(key_str)
                except ValueError as e:
                    logger.error(
                        f"Failed to parse message key to request ID: {e}"
                    )
                    return

            response = moderation_pb2.ModerateObjectResponse()
            response.ParseFromString(msg.value())

            logger.info(
                f"Received moderation response: request_id={request_id}, "
                f"success={response.success}"
            )

            if self.callback:
                try:
                    self.callback(response, request_id)
                except Exception as e:
                    logger.error(f"Error in callback: {e}")

        except Exception as e:
            logger.error(f"Failed to process message: {e}")

    def is_running(self) -> bool:
        return self.running
