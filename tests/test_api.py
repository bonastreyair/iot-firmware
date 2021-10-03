import pytest
from marshmallow import ValidationError

from iot_firmware.communications.schema import API_VERSION
from iot_firmware.communications.schema import Message
from iot_firmware.enums import MessageKey
from iot_firmware.enums import MessageType


def test_load_message():
    message = Message.load({MessageKey.TYPE: MessageType.READING, MessageKey.DATA: {}})
    assert message.api_version == API_VERSION


def test_missing_type():
    with pytest.raises(ValidationError, match=MessageKey.TYPE):
        Message.load({MessageKey.DATA: {}})


def test_missing_data():
    with pytest.raises(ValidationError, match=MessageKey.DATA):
        Message.load({MessageKey.TYPE: MessageType.READING})
