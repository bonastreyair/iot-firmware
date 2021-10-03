from typing import Dict

device_id = 0


def read_config(config: Dict):
    global device_id
    device_id = 0
    return config


def get_device_id():
    global device_id
    return device_id
