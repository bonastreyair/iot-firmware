from enum import Enum
from enum import EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class StringEnum(str, Enum, metaclass=MetaEnum):
    def __str__(self):
        return "%s" % self.value

    def __repr__(self):
        return "'%s'" % self.value


class MessageType(StringEnum):
    READING = "reading"
    EVENT = "event"
    COMMAND = "command"
    ACK = "ack"


class Counter:
    def __init__(self, start: int = 0):
        self._value = start

    def __call__(self):
        self._value += 1
        return self._value
