import pytest
from marshmallow import ValidationError

from iot_firmware.communications.API import API_VERSION
from iot_firmware.communications.API import load_message
from iot_firmware.communications.API import MessageType
from iot_firmware.communications.enums import MessageKey


def test_load_message():
    message = load_message({MessageKey.TYPE: MessageType.READING, MessageKey.DATA: {}})
    assert message.api == API_VERSION


def test_missing_type():
    with pytest.raises(ValidationError, match=MessageKey.TYPE):
        load_message({MessageKey.DATA: {}})


def test_missing_data():
    with pytest.raises(ValidationError, match=MessageKey.DATA):
        load_message({MessageKey.TYPE: MessageType.READING})
