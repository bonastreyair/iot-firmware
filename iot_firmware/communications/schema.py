"""Module with the schemas related with the communications package."""
import time
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Dict

import marshmallow_dataclass
from marshmallow import validate

from ..enums import MessageType
from .utils import Counter
from iot_firmware.schema import get_device_id

msg_id_counter = Counter()


@dataclass
class Version:
    """Semantic Versioning following https://semver.org.

    :param major: incompatible API changes
    :param minor: new functionality (backwards compatible)
    :param patch: bug fixes (backwards compatible)

    Usage:

    >>> ver = Version(major=1, minor=2, patch=3)
    >>> ver
    1.2.3
    """

    major: int = field(
        metadata={
            "required": True,
            "strict": True,
        }
    )
    minor: int = field(
        metadata={
            "required": True,
            "strict": True,
        }
    )
    patch: int = field(
        metadata={
            "required": True,
            "strict": True,
        }
    )

    def __repr__(self):
        """Representation of the version."""
        return f"{self.major}.{self.minor}.{self.patch}"


API_VERSION = Version(0, 0, 1)


@dataclass
class Message:
    """Message for external communications.

    Basic usage.

    >>> message = Message.load({"type": MessageType.READING, "data": {"temp": 24.3}})
    >>> message.api_version
    0.0.1
    >>> message.data
    {'temp': 24.3}
    """

    type: str = field(
        metadata={
            "required": True,
            "validate": validate.OneOf(MessageType),
            "metadata": {"description": "the type of the message"},
        }
    )
    data: Any = field()

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
    api_version: Version = field(
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

    @classmethod
    def load(cls, message: Dict) -> "Message":
        """Loads a dict to a Message class and creates an instance of it.

        :param message: dict of the data
        """

        schema = marshmallow_dataclass.class_schema(cls)()
        return schema.load(message)
