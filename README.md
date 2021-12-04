# iot-firmware ![](https://findicons.com/files/icons/42/basic/16/warning.png)

> **WARNING**: Package under development...

[![](https://img.shields.io/readthedocs/iot-firmware/latest?logo=readthedocs)](https://iot-firmware.readthedocs.io/en/latest/)
[![](https://results.pre-commit.ci/badge/github/bonastreyair/iot-firmware/main.svg)](https://results.pre-commit.ci/latest/github/bonastreyair/iot-firmware/main)
[![](https://img.shields.io/github/workflow/status/bonastreyair/iot-firmware/CI?label=CI&logo=github)](https://github.com/bonastreyair/iot-firmware/actions?workflow=CI)
[![](https://img.shields.io/codecov/c/github/bonastreyair/iot-firmware/main?logo=codecov)](https://codecov.io/gh/bonastreyair/iot-firmware)
[![](https://img.shields.io/codeclimate/maintainability/bonastreyair/iot-firmware?logo=codeclimate)](https://codeclimate.com/github/bonastreyair/iot-firmware/maintainability)
[![](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![](https://img.shields.io/github/license/bonastreyair/iot-firmware?color=blue)](https://github.com/bonastreyair/iot-firmware/blob/main/LICENSE)

It provides a set of tools to simplify the creation, configuration of and IoT Firmware
in the most robust and easy way. It uses async for all its operations. It requires Python 3.8+.

All notable changes to this project will be documented in the [CHANGELOG.md](https://github.com/bonastreyair/iot-firmware/blob/main/CHANGELOG.md) file.

Documentation is available at [Read the Docs](https://iot-firmware.readthedocs.io/en/latest/).

## Install

Library can be installed in many ways.

### Python Package

#### PyPI

Install the latest pip package from GitHub.

```sh
pip install git+ssh://git@github.com/bonastreyair/iot-firmware.git
```

#### Local

It is required to clone the repo and then install from local.

```sh
pip install .
```

## Usage

### CLI - Command-line Interface

```sh
iot-firmware -h
```

```text
usage: iot-firmware [-h] [-v] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c CONFIG, --config CONFIG
                        path to the configuration
```

### Python Code

```python
from iot_firmware import Controller

config = {}

fw = Controller(config)
fw.start()
```

## Contribute

### Pre-commit

Make sure to run `pre-commit run --all-files` before any `Pull Request`. If you want you can set it up automatically
in local before any commit with the following command.

```sh
pre-commit install
```

### Tests

Make sure to run the tests using `pytest`. You can install the package dependencies with the `[test]` option
so that you can run the test in local.

```sh
pip install .[test]
```

### Docs

To build the docs in local you will need to install the package with the `[docs]` option.

```sh
pip install .[docs]
```

Then you can build it with

```sh
cd docs
python generate_graphs.py
make html
open build/html/index.html
```
