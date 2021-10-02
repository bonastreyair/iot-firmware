import abc
import time
import uuid
from dataclasses import dataclass
from typing import Any

from .enum import EventLevel
from .type import EventType
from iot_firmware.enums import TIME_FORMAT


@dataclass
class Event(abc.ABC):
    """Abstract class for any Event class.

    It contain a custom name and any data as well as a level of an event
    (default is INFO).
    """

    data: Any = None
    level: EventLevel = EventLevel.INFO

    @property
    @abc.abstractmethod
    def type(self) -> EventType:
        """Event Type.

        Must be defined.
        """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the Event.

        Must be defined.
        """

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
