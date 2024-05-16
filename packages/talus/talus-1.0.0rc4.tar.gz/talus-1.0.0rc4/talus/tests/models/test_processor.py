"""Tests for the message processor models."""
from typing import Type
from uuid import uuid4

import pika
import pytest

from talus.models.message import ConsumeMessageBase
from talus.models.processor import DLQMessageProcessor
from talus.models.processor import MessageProcessorBase
from talus.models.processor import MessageProcessorRoutingKeySelector


@pytest.fixture()
def successful_message_processor(consume_message_cls) -> MessageProcessorBase:
    """
    A message processor that does not raise an exception.
    """

    class SuccessfulMessageProcessor(MessageProcessorBase):
        message_cls: Type[ConsumeMessageBase] = consume_message_cls

        def process_message(self, message: ConsumeMessageBase):
            self._message_was_processed = True

    yield SuccessfulMessageProcessor()


@pytest.fixture()
def consumed_message(
    publish_message_cls,
    producer,
    consumer,
    body,
) -> tuple[pika.spec.Basic.Deliver, pika.spec.BasicProperties, bytes]:
    outbound_message = publish_message_cls(body=body)
    producer.publish(message=outbound_message)
    for m, p, b in consumer.consume_generator(auto_ack=True):
        yield m, p, b  # only the first one
        break


def test_message_processor_success(consumer, consumed_message, successful_message_processor):
    """
    :given: A message processor that does not raise an exception.
    :when: The message processor is called.
    :then: The message processor should process and acknowledge the message.
    """
    # given
    method, properties, body = consumed_message
    # when
    successful_message_processor(
        channel=consumer.channel, method=method, properties=properties, body=body
    )
    # then
    assert successful_message_processor._message_was_processed
    assert not consumer.channel.get_waiting_message_count()  # no messages left in the queue


@pytest.fixture()
def erroring_message_processor(consume_message_cls) -> MessageProcessorBase:
    """
    A message processor that raises a non-dead-letter exception.
    """

    class ErroringMessageProcessor(MessageProcessorBase):
        message_cls: Type[ConsumeMessageBase] = consume_message_cls
        dead_letter_exceptions: Type[Exception] = ValueError

        def process_message(self, message: ConsumeMessageBase):
            raise RuntimeError("A bad message processor raised an exception that is not DLQ'd.")

    yield ErroringMessageProcessor()


def test_message_processor_failure(erroring_message_processor, consumed_message, consumer):
    """
    :given: A message processor that raises an exception.
    :when: The message processor is called.
    :then: Expected exception is raised.
    """
    # given
    method, properties, body = consumed_message
    # when/then
    with pytest.raises(RuntimeError):
        erroring_message_processor(
            channel=consumer.channel, method=method, properties=properties, body=body
        )


@pytest.fixture()
def dlq_message_processor(consume_message_cls) -> DLQMessageProcessor:
    """
    A message processor that raises a non-dead-letter exception.
    """

    class AutoDLQMessageProcessor(DLQMessageProcessor):
        message_cls: Type[ConsumeMessageBase] = consume_message_cls
        dead_letter_exceptions: Type[Exception] = RuntimeError

        def process_message(self, message: ConsumeMessageBase):
            self._raised_run_time_error = True
            raise RuntimeError("A bad message processor raised an exception that is DLQ'd.")

    yield AutoDLQMessageProcessor()


def test_dlq_message_processor(dlq_message_processor, consumed_message, consumer):
    """
    :given: A message processor that raises an exception identified as for DLQ.
    :when: The message processor is called.
    :then: The message processor should DLQ the message.
    """
    # given
    method, properties, body = consumed_message
    # when
    dlq_message_processor(channel=consumer.channel, method=method, properties=properties, body=body)
    # then
    assert dlq_message_processor._raised_run_time_error
    assert not consumer.channel.get_waiting_message_count()  # no messages left in the queue


@pytest.fixture()
def message_processor_routing_key_selector(
    routing_key, successful_message_processor
) -> MessageProcessorRoutingKeySelector:
    """
    A message processor selector that selects a message processor based on the routing key.
    """
    return MessageProcessorRoutingKeySelector(
        message_processors={
            routing_key: successful_message_processor,
        }
    )


def test_message_processor_routing_key_selector_found(
    message_processor_routing_key_selector, consumed_message, consumer, successful_message_processor
):
    """
    :given: A message processor selector that selects a message processor based on the routing key.
    :when: The message processor selector is called with a message of that routing key.
    :then: The expected message processor should be run and returned.
    """
    # given
    method, properties, body = consumed_message
    # when
    message_processor = message_processor_routing_key_selector(
        channel=consumer.channel, method=method, properties=properties, body=body
    )
    # then
    assert not consumer.channel.get_waiting_message_count()  # no messages left in the queue
    assert isinstance(message_processor, type(successful_message_processor))


def test_message_processor_routing_key_selector_not_found(
    message_processor_routing_key_selector, consumer, consumed_message
):
    """
    :given: A message processor selector that selects a message processor based on the routing key.
    :when: The message processor selector is called with a message an unknown routing key.
    :then: The DLQ message processor should be returned.
    """
    # given
    method, properties, body = consumed_message
    unknown_routing_key = uuid4().hex
    method.routing_key = unknown_routing_key
    # when/then
    message_processor = message_processor_routing_key_selector(
        channel=consumer.channel, method=method, properties=properties, body=body
    )
    # then
    assert not consumer.channel.get_waiting_message_count()  # no messages left in the queue
    assert isinstance(message_processor, DLQMessageProcessor)
