from ..utils import StringEnum


class MessageKey(StringEnum):
    TYPE = "type"
    DATA = "data"

    ID = "id"
    TIMESTAMP = "timestamp"
    API = "api"
    MSG_ID = "msg_id"


class MessageType(StringEnum):
    READING = "reading"
    EVENT = "event"
    COMMAND = "command"
    ACK = "ack"


class CommandType(StringEnum):
    CONFIG = "config"
    DEVICE = "device"
    REBOOT = "reboot"
