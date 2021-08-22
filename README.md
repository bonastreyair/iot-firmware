# iot-firmware

It provides a set of tools to simplify the creation, configuration of and IoT Firmware
in the most robust and easy way. It uses async for all its operations.

It requires Python 3.7+.

## Install

```shell
pip install iot_firmware
```

## Usage

```python
from iot_firmware.firmware import Firmware

config = {}

fw = Firmware(config)
fw.run()
```


## Contribute

```shell
pre-commit install
```
