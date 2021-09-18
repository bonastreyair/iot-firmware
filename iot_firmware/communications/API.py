import time
from dataclasses import dataclass
from dataclasses import field
from typing import Dict

import marshmallow_dataclass
from marshmallow import validate

from ..core.config import get_device_id
from ..utils import Counter
from .enums import MessageType

API_VERSION = [0, 0, 1]

msg_id_counter = Counter()


@dataclass
class Message:
    type: str = field(
        metadata={
            "required": True,
            "validate": validate.OneOf(MessageType),
            "metadata": {"description": "the type of the message"},
        }
    )
    data: dict = field()

    # Automatic fields
    id: int = field(
        metadata={
            "required": False,
            "load_default": lambda: get_device_id(),
            "validate": validate.Range(min=0),
            "metadata": {"description": "the configured device id"},
        }
    )
    timestamp: float = field(
        metadata={
            "required": False,
            "load_default": lambda: time.time(),
            "validate": validate.Range(min=0),
        }
    )
    api: list = field(
        metadata={
            "required": False,
            "load_default": API_VERSION,
        }
    )
    msg_id: int = field(
        metadata={
            "required": False,
            "load_default": lambda: msg_id_counter(),
            "validate": validate.Range(min=0),
        }
    )


def load_message(message: Dict) -> Message:
    schema = marshmallow_dataclass.class_schema(Message)()
    return schema.load(message)
