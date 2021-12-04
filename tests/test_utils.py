from enum import Enum

from iot_firmware.enums import ContainsEnumMeta


def test_meta_enum():
    class NewEnum(str, Enum, metaclass=ContainsEnumMeta):
        A = "a"

    assert "a" in NewEnum
    assert "c" not in NewEnum
