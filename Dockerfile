ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION as builder

COPY setup.cfg setup.py pyproject.toml README.md LICENSE .
COPY iot_firmware /iot_firmware
RUN pip install --upgrade build
RUN python -m build

FROM python:${PYTHON_VERSION}-slim

COPY --from=builder /dist/iot_firmware-*.whl /tmp/.

RUN pip install /tmp/iot_firmware-*.whl; rm /tmp/iot_firmware-*.whl

ENTRYPOINT [ "iot-firmware" ]
