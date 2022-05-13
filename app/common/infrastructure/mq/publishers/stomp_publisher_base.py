"""
This module defines a StompPublisherBase, which is an abstract class intended
to define common behavior for stomp-implemented MQ publisher components.
"""
import json
from abc import ABC

from app.common.domain.mq.exceptions.mq_message_publish_exception import MqMessagePublishException
from app.common.infrastructure.mq.stomp_interactor import StompInteractor


class StompPublisherBase(StompInteractor, ABC):

    def _publish_message(self, message: dict) -> None:
        """
        Publishes a message to the queue.

        :param message: message to publish as dictionary
        :type message: dict

        :raises MqMessagePublishException
        """
        connection = self._create_mq_connection()
        try:
            self.__add_message_retrying_admin_metadata(message)
            message_json_str = json.dumps(message)
            connection.send(destination=self._get_queue_name(), body=message_json_str)
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
