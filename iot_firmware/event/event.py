import uuid

from .core import Event
from .core import EventType


# Event Types
class ReadingEventType(EventType):
    uuid = uuid.uuid4()

    def __init__(self):
        super().__init__(name="reading")


class CommandEventType(EventType):
    uuid = uuid.uuid4()

    def __init__(self):
        super().__init__(name="command")


# Events
class ReadingEvent(Event):
    type = ReadingEventType()


class CommandEvent(Event):
    type = CommandEventType()
