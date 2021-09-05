# iot-firmware [under development...]

It provides a set of tools to simplify the creation, configuration of and IoT Firmware
in the most robust and easy way. It uses async for all its operations. It requires Python 3.8+.

The [Official Documentation](https://bonastreyair.github.io/iot-firmware/iot_firmware.html) 
is being stored using GitHub Pages.

## Install

Library can be installed in many ways.

### Python Package

#### PyPI

```shell
pip install iot_firmware
```

#### Local

```shell
pip install . --use-feature=in-tree-build
```

### Docker Image (Python based)

A docker image is also available, for a `Python 3.8-slim` execution you can just run:
```shell
docker build -t iot-firmware --build-arg PYTHON_TAG=3.8-slim .
```

## Usage

### CLI - Command-line Interface

```
iot-firmware -h

usage: iot-firmware [-h] [-v] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c CONFIG, --config CONFIG
                        path to the configuration
```

### Docker Image

```
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
from iot_firmware import Firmware

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

