import logging
from enum import Enum
from enum import IntEnum


class EventLevel(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class EventTypeName(Enum):
    READING = "reading"
    COMMAND = "command"
