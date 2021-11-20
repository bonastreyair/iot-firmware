from enum import Enum
from enum import EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item) -> bool:
        try:
            cls(item)
        except ValueError:
            return False
        return True


class StrEnum(str, Enum, metaclass=MetaEnum):
    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"'{self.value}'"


class MessageType(StrEnum):
    READING = "reading"
    EVENT = "event"
    COMMAND = "command"
    ACK = "ack"


class MessageKey(StrEnum):
    TYPE = "type"
    DATA = "data"

    ID = "id"
    TIMESTAMP = "timestamp"
    API = "api"
    MSG_ID = "msg_id"


class CommandType(StrEnum):
    CONFIG = "config"
    DEVICE = "device"
    REBOOT = "reboot"


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
