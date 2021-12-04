import pytest

from iot_firmware import Controller


@pytest.fixture(params=[{}, {"mock_config": "mock"}])
def config(request):
    return request.param


def test_firmware_run():
    fw = Controller()
    fw.start()
    with pytest.raises(RuntimeError):
        fw.start()
    fw.stop()


def test_firmware_with_config(config):
    fw = Controller(config)
    assert fw.config == config
