from enum import Enum

from iot_firmware.utils import MetaEnum


def test_meta_enum():
    class NewEnum(str, Enum, metaclass=MetaEnum):
        A = "a"

    assert "a" in NewEnum
    assert "c" not in NewEnum
