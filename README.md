# iot-firmware [under development...]

[![CI](https://github.com/bonastreyair/iot-firmware/workflows/CI/badge.svg)](https://github.com/bonastreyair/iot-firmware/actions)
[![Documentation Status](https://readthedocs.org/projects/iot-firmware/badge/?version=latest)](https://iot-firmware.readthedocs.io/en/latest/?badge=latest)
[![coverage](https://img.shields.io/codecov/c/github/bonastreyair/iot-firmware/main)](https://codecov.io/gh/bonastreyair/iot-firmware)
[![code_style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![license](https://img.shields.io/github/license/bonastreyair/iot-firmware)](https://github.com/bonastreyair/iot-firmware/blob/main/LICENSE)

It provides a set of tools to simplify the creation, configuration of and IoT Firmware
in the most robust and easy way. It uses async for all its operations. It requires Python 3.8+.


## Install

Library can be installed in many ways.

### Python Package

#### PyPI

```shell
pip install iot_firmware
```

#### Local

```shell
pip install .
```

### Docker Image (Python based)

A docker image is also available, for a `Python 3.8-slim` execution you can just run:
```shell
docker build -t iot-firmware --build-arg PYTHON_TAG=3.8-slim .
```

## Usage

### CLI - Command-line Interface

```text
iot-firmware -h

usage: iot-firmware [-h] [-v] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c CONFIG, --config CONFIG
                        path to the configuration
```

### Docker Image

```text
docker run --rm iot-firmware -h

usage: iot-firmware [-h] [-v] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c CONFIG, --config CONFIG
                        path to the configuration
```

### Python Code

```python
from iot_firmware.core import Firmware

config = {}

fw = Firmware(config)
fw.run()
```

## Contribute

### Pre-commit

Make sure to run `pre-commit run --all-files` before any `Pull Request`. If you want you can set it up automatically
in local before any commit with the following command.
```shell
pre-commit install
```

### Tests

Make sure to run the tests using `pytest`. You can install the package dependencies with the `[test]` option
so that you can run the test in local.
```shell
pip install -e .[test]
```
