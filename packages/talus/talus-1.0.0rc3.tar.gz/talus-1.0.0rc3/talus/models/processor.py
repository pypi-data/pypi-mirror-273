"""Base Processor for messages consumed from a channel."""
import logging
from abc import ABC
from abc import abstractmethod
from typing import Type

import pika
from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError

from talus.models.message import ConsumeMessageBase

logger = logging.getLogger(__name__)


DEFAULT_DEAD_LETTER_EXCEPTIONS = (ValidationError,)


class MessageProcessorBase(BaseModel, ABC):
    message_cls: Type[ConsumeMessageBase]
    dead_letter_exceptions: Type[Exception] | tuple[Type[Exception]] = Field(
        default=DEFAULT_DEAD_LETTER_EXCEPTIONS
    )

    @abstractmethod
    def process_message(self, message: ConsumeMessageBase):
        pass  # pragma: no cover

    @classmethod
    def dlq_message(
        cls,
        channel: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        exception: Exception | None = None,
    ) -> None:
        logger.warning(f"Dead lettering message:{method=}, {properties=}, {exception=}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    @classmethod
    def acknowledge_message(
        cls, channel: pika.adapters.blocking_connection.BlockingChannel, message: ConsumeMessageBase
    ) -> None:
        logger.debug(
            f"Acknowledging message: method={message.method}, properties={message.properties}, {message=}"
        )
        channel.basic_ack(delivery_tag=message.delivery_tag)

    def __call__(
        self,
        channel: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> "MessageProcessorBase":
        try:
            message = self.message_cls(method=method, properties=properties, body=body)
            self.process_message(message)
            self.acknowledge_message(channel=channel, message=message)
        except self.dead_letter_exceptions as e:
            self.dlq_message(channel=channel, method=method, properties=properties, exception=e)
        return self


class DLQMessageProcessor(MessageProcessorBase):
    message_cls: Type[ConsumeMessageBase] = ConsumeMessageBase
    dead_letter_exceptions: Type[Exception] | tuple[Type[Exception]] = Field(
        default_factory=lambda: DEFAULT_DEAD_LETTER_EXCEPTIONS + (ValueError,)
    )

    def process_message(self, message: ConsumeMessageBase):
        raise ValueError(f"DLQMessageProcessor auto fails processing: {message=}")


class MessageProcessorSelectorBase(BaseModel, ABC):
    message_processors: dict[str, MessageProcessorBase]

    @abstractmethod
    def get_message_processor(
        self,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> MessageProcessorBase:
        pass  # pragma: no cover

    def __call__(
        self,
        channel: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> MessageProcessorBase:
        message_processor = self.get_message_processor(
            method=method, properties=properties, body=body
        )
        return message_processor(channel=channel, method=method, properties=properties, body=body)


class MessageProcessorRoutingKeySelector(MessageProcessorSelectorBase):
    def get_message_processor(
        self,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> MessageProcessorBase:
        routing_key = method.routing_key

        message_processor = self.message_processors.get(routing_key)
        if message_processor is None:
            logger.error(f"No message processor found for routing key: {routing_key}")
            message_processor = DLQMessageProcessor()
        return message_processor
