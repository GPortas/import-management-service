"""
This module defines a TransferStatusQueueListener, which defines the necessary
logic to connect to the remote MQ and listen for transfer status messages.
"""
import os

from stomp.utils import Frame

from app.ingest.application.mq.mq_connection_params import MqConnectionParams
from app.ingest.application.mq.listeners.stomp_listener_base import StompListenerBase


class TransferStatusQueueListener(StompListenerBase):

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_TRANSFER_QUEUE_TRANSFER_STATUS')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_TRANSFER_HOST'),
            mq_port=os.getenv('MQ_TRANSFER_PORT'),
            mq_ssl_enabled=os.getenv('MQ_TRANSFER_SSL_ENABLED'),
            mq_user=os.getenv('MQ_TRANSFER_USER'),
            mq_password=os.getenv('MQ_TRANSFER_PASSWORD')
        )

    def _handle_received_message(self, frame: Frame) -> None:
        pass

    def _handle_received_error(self, frame: Frame) -> None:
        pass
