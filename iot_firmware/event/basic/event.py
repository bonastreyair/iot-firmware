from ..event import Event
from .type import CommandEventType
from .type import ReadingEventType


class ReadingEvent(Event):
    name = ReadingEventType.name
    type = ReadingEventType


class CommandEvent(Event):
    name = CommandEventType.name
    type = CommandEventType
