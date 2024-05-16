"""
Module encapsulating message structure to facilitate use with the Consumer and Producer wrappers
"""
import uuid
from typing import Type

import pika.spec
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class MessageBodyBase(BaseModel):
    """
    Base class for message schemas which can be used to validate message bodies.
    """

    model_config = ConfigDict(extra="allow")

    conversation_id: str = Field(default_factory=lambda: uuid.uuid4().hex, alias="conversationId")


class MessageBase:
    """
    Base class for messages establishing a common interface for use by DurableConnections
    """

    message_body_cls: Type[MessageBodyBase] = MessageBodyBase

    def __init__(self, routing_key: str, body: bytes | dict | str | MessageBodyBase):
        self.routing_key = routing_key
        if isinstance(body, dict | BaseModel):
            self.body: MessageBodyBase = self.message_body_cls.model_validate(body)
        else:  # str | bytes
            self.body: MessageBodyBase = self.message_body_cls.model_validate_json(body)


class ConsumeMessageBase(MessageBase):
    """
    Base class for messages consumed from a DurableConsumer MessageProcessor.
    TODO example of how to use this class
    """

    def __init__(
        self,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes | dict | str | MessageBodyBase,
    ):
        super().__init__(method.routing_key, body)
        self.method = method
        self.properties = properties

    @property
    def delivery_tag(self):
        return self.method.delivery_tag

    @property
    def headers(self) -> dict | None:
        return self.properties.headers


class PublishMessageBase(MessageBase):
    """
    Base class for messages published to with a DurableProducer
    """

    routing_key: str = "default.m"
    headers: dict[str, str] | None = (None,)

    def __init__(
        self,
        body: bytes | dict | str | MessageBodyBase,
    ):
        super().__init__(self.routing_key, body)

    @property
    def properties(self) -> pika.spec.BasicProperties:
        return pika.BasicProperties(
            content_type="text/plain",
            priority=0,
            delivery_mode=pika.DeliveryMode.Persistent,
            content_encoding="UTF-8",
            headers=self.headers,
        )
