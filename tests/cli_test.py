import pytest

from iot_firmware import __version__
from iot_firmware.cli import cli


def test_version(capsys):
    with pytest.raises(SystemExit):
        cli(["-v"])
    out, _ = capsys.readouterr()
    assert out == f"iot-firmware {__version__}\n"
