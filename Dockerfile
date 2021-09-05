ARG PYTHON_TAG
FROM python:${PYTHON_TAG} as builder

COPY setup.cfg setup.py pyproject.toml README.md LICENSE ./
COPY iot_firmware /iot_firmware
RUN pip install --upgrade build
RUN python -m build

# Docker Image
FROM python:${PYTHON_TAG}

COPY --from=builder /dist/iot_firmware-*.whl /tmp/.
RUN pip install /tmp/iot_firmware-*.whl; rm /tmp/iot_firmware-*.whl

ENTRYPOINT [ "iot-firmware" ]
