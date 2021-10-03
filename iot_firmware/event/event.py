import abc
import time
import uuid
from typing import Any

from .enum import EventLevel
from .type import EventType
from iot_firmware.enums import TIME_FORMAT


class Event(abc.ABC):
    """Abstract class for any Event class.

    Contains a custom name and any data as well as a level of an event.
    """

    type: EventType
    name: str
    uuid: str
    timestamp: float

    def __init__(self, data: Any = None, level: EventLevel = EventLevel.INFO) -> None:
        self.data = data
        self.level = level
        self.__post_init__()

    @property
    @abc.abstractmethod
    def type(self) -> EventType:
        """Event Type."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the Event."""

    def __post_init__(self) -> None:
        """Every event will have a universally unique identifier as well as an
        timestamp of the event."""
        self.__uuid = str(uuid.uuid4())
        self.__timestamp = time.time()

    @property
    def uuid(self) -> str:
        """Universally unique identifier of the event."""
        return self.__uuid

    @property
    def timestamp(self) -> float:
        """Timestamp of the event."""
        return self.__timestamp

    def __repr__(self) -> str:
        time_format = time.strftime(TIME_FORMAT, time.gmtime(self.timestamp))
        return f"{self.level.name}: {time_format} [{self.name} {self.type.name} EVENT]: {self.data}"
