"""Event Enums."""
from iot_firmware.enums import StrEnum


class EventLevel(StrEnum):
    """Event levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
