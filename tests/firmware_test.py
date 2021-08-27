import pytest

from iot_firmware.firmware import Firmware


@pytest.fixture(params=[{}, {"mock_config": "mock"}])
def config(request):
    return request.param


def test_firmware_run():
    fw = Firmware()
    fw.run()
    with pytest.raises(RuntimeError):
        fw.run()
    fw.stop()


def test_firmware_with_config(config):
    fw = Firmware(config)
    assert fw.config == config
