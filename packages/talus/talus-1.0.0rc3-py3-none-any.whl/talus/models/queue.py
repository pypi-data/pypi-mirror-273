"""Queue model."""
from pydantic import BaseModel


class Queue(BaseModel):
    """Queue model."""

    name: str
    passive: bool = False
    durable: bool = True
    auto_delete: bool = False
    exclusive: bool = False
    arguments: dict | None = None  # TODO https://www.rabbitmq.com/docs/quorum-queues#declaring

    def __str__(self):
        return self.name
