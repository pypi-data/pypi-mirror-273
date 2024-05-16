"""
Bindings contain the many-to-many relationship between a message routing key and a queue on an exchange.
"""
from typing import Type

from pydantic import AfterValidator
from pydantic import BaseModel
from pydantic import ConfigDict
from typing_extensions import Annotated

from talus.models.message import PublishMessageBase
from talus.models.queue import Queue


def validate_routing_key(message: Type[PublishMessageBase]):
    if not message.routing_key:
        raise ValueError("routing_key must not be empty")
    return message


class Binding(BaseModel):
    """Binding configuration."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    message: Annotated[Type[PublishMessageBase], AfterValidator(validate_routing_key)]
    queue: Queue

    @property
    def routing_key(self) -> str:
        return self.message.routing_key

    @property
    def queue_name(self) -> str:
        return self.queue.name
