"""Event Enums."""
import logging
from enum import IntEnum


class EventLevel(IntEnum):
    """Event levels."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
