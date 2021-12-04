"""Event Enums."""
from enum import auto
from enum import Enum

from iot_firmware.enums import StrEnum


class EventLevel(StrEnum):
    """Event levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EventHandlerState(Enum):
    """EventHandler possible states."""

    IDLE = auto()
    RUNNING = auto()
    STOPPING = auto()
