"""
This module defines a StompPublisherBase, which is an abstract class intended
to define common behavior for stomp-implemented MQ publisher components.
"""
import json
import os
import time
from abc import ABC

from app.common.domain.mq.exceptions.mq_message_publish_exception import MqMessagePublishException
from app.common.infrastructure.mq.stomp_interactor import StompInteractor


class StompPublisherBase(StompInteractor, ABC):
    __DEFAULT_MESSAGE_EXPIRATION_MS = 3600000

    def _publish_message(self, message: dict) -> None:
        """
        Publishes a message to the queue.

        :param message: message to publish as dictionary
        :type message: dict

        :raises MqException
        """
        connection = self._create_mq_connection()
        try:
            self.__add_message_retrying_admin_metadata(message)
            message_json_str = json.dumps(message)
            connection.send(
                destination=self._get_queue_name(),
                body=message_json_str,
                headers={
                    "persistent": "true",
                    "expires": self.__get_message_expiration_limit_ms()
                }
            )
        except Exception as e:
            self._logger.error(str(e))
            mq_connection_params = self._get_mq_connection_params()
            raise MqMessagePublishException(
                queue_name=self._get_queue_name(),
                queue_host=mq_connection_params.mq_host,
                queue_port=mq_connection_params.mq_port,
                reason=str(e)
            )
        finally:
            self._logger.debug("Disconnecting from MQ...")
            connection.disconnect()

    def __add_message_retrying_admin_metadata(self, message: dict) -> None:
        """
        Adds retrying admin metadata fields to the body of the message to be sent.
        """
        message['admin_metadata'] = message.get('admin_metadata', {}) | {
            'original_queue': self._get_queue_name(),
            'retry_count': 0
        }

    def __get_message_expiration_limit_ms(self) -> int:
        """
        Retrieves the message expiration limit in milliseconds.
        """
        now_ms = int(time.time()) * 1000
        message_expiration_ms = int(os.getenv('MESSAGE_EXPIRATION_MS', self.__DEFAULT_MESSAGE_EXPIRATION_MS))
        message_expiration_limit_ms = now_ms + message_expiration_ms
        return message_expiration_limit_ms
