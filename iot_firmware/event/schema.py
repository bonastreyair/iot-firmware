"""Module with the schemas related with the event package."""
import abc
import time
import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Protocol

from .enum import EventLevel


class EventTypeMeta(type):
    """Meta class for event types.

    It generates a uuid for each unique event type class.
    """

    uuid: str

    def __init__(cls, what, bases, dct) -> None:
        super().__init__(what, bases, dct)
        cls.uuid: str = str(uuid.uuid4())

    def __repr__(cls) -> str:
        return f"'{cls.__name__}'"


class EventType(metaclass=EventTypeMeta):
    """Abstract class for any Event type class."""


@dataclass
class Event(abc.ABC):
    """Abstract class for any Event class.

    Contains a custom name and any data as well as a level of an event.

    :param data: Any data in any format
    :param level: level of the event (default INFO)
    """

    data: Any = field(init=True, repr=True, default=None)
    level: EventLevel = field(init=True, repr=True, default=EventLevel.INFO)
    timestamp: float = field(init=False, repr=False, default_factory=time.time)
    uuid: str = field(init=False, repr=False, default_factory=lambda: str(uuid.uuid4()))

    @property
    @abc.abstractmethod
    def type(self) -> EventType:
        """Event Type."""


class CallableEventFunction(Protocol):
    @staticmethod
    def __call__(event: Event) -> Any:
        ...
