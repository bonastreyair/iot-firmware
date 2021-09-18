ARG PYTHON_TAG
FROM python:${PYTHON_TAG} as builder

RUN pip install --upgrade build
COPY setup.cfg pyproject.toml README.md CHANGELOG.md LICENSE.md ./
COPY iot_firmware /iot_firmware
RUN python -m build

# Docker Image
FROM python:${PYTHON_TAG}

COPY --from=builder /dist/iot_firmware-*.whl /tmp/.
RUN pip install /tmp/iot_firmware-*.whl; rm /tmp/iot_firmware-*.whl

ENTRYPOINT [ "iot-firmware" ]
