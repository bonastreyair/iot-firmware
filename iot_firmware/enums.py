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


class MessageType(StringEnum):
    READING = "reading"
    EVENT = "event"
    COMMAND = "command"
    ACK = "ack"


class MessageKey(StringEnum):
    TYPE = "type"
    DATA = "data"

    ID = "id"
    TIMESTAMP = "timestamp"
    API = "api"
    MSG_ID = "msg_id"


class CommandType(StringEnum):
    CONFIG = "config"
    DEVICE = "device"
    REBOOT = "reboot"
