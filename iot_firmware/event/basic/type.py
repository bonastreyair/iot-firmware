from ..enum import EventTypeName
from ..type import EventType


class ReadingEventType(EventType):
    name: str = EventTypeName.READING


class CommandEventType(EventType):
    name: str = EventTypeName.COMMAND
