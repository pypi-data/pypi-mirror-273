"""Retryer Factory Model."""
import logging

from pika.exceptions import AMQPHeartbeatTimeout
from pika.exceptions import ChannelClosed
from pika.exceptions import ChannelClosedByClient
from pika.exceptions import ChannelError
from pika.exceptions import ChannelWrongStateError
from pika.exceptions import ConnectionBlockedTimeout
from pika.exceptions import ConnectionClosedByClient
from pika.exceptions import ConnectionOpenAborted
from pika.exceptions import ConnectionWrongStateError
from pika.exceptions import InvalidChannelNumber
from pika.exceptions import NoFreeChannels
from pika.exceptions import StreamLostError
from pika.exceptions import UnexpectedFrameError
from pydantic import BaseModel
from tenacity import after_log
from tenacity import retry_if_exception_type
from tenacity import Retrying
from tenacity import stop_after_attempt
from tenacity import wait_exponential
from tenacity import wait_random

logger = logging.getLogger(__name__)


class RetryerFactory(BaseModel):
    """Translator for the retry configuration to a tenacity.Retrying object."""

    delay_min: int = 1
    delay_max: int = 300
    jitter_min: int = 1
    jitter_max: int = 10
    attempts: int = -1  # -1 means retry forever
    exceptions: type[Exception] | tuple[type[Exception], ...] = type(
        Exception
    )  # retry any exception

    def __call__(self) -> Retrying:
        """
        Returns a tenacity.Retrying object based on the configuration.
        """
        wait = wait_exponential(
            multiplier=self.delay_min,
            min=self.delay_min,
            max=self.delay_max,
        ) + wait_random(self.jitter_min, self.jitter_max)
        stop = None
        if self.attempts > -1:
            stop = stop_after_attempt(self.attempts)
        return Retrying(
            retry=retry_if_exception_type(self.exceptions),
            wait=wait,
            stop=stop,
            after=after_log(logger=logger, log_level=logging.INFO),
        )


DEFAULT_CONNECTION_EXCEPTIONS = (
    ConnectionOpenAborted,
    StreamLostError,
    NoFreeChannels,
    ConnectionWrongStateError,
    ConnectionClosedByClient,
    ConnectionBlockedTimeout,
    AMQPHeartbeatTimeout,
    ChannelWrongStateError,
    ChannelClosed,
    ChannelClosedByClient,
    InvalidChannelNumber,
    UnexpectedFrameError,
    ChannelError,
)


class ConnectionRetryerFactory(RetryerFactory):
    exceptions: type[Exception] | tuple[type[Exception], ...] = DEFAULT_CONNECTION_EXCEPTIONS
