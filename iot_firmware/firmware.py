import asyncio
import logging
from typing import Dict

import uvloop

from .communications.task import communications_task
from .core.config import read_config
from .core.task import core_task
from .devices.task import devices_task
from .monitor.task import events_task


class Firmware:
    def __init__(self, config: Dict = None):
        uvloop.install()
        self.config = read_config(config)
        self.async_coroutines = []

        # Queue instances
        self.q_control = None
        self.q_measurements = None
        self.q_actions = None
        self.q_send = None
        self.q_events = None

        # Async Tasks
        self.control_task = None
        self.devices_task = None
        self.report_task = None
        self.communications_task = None

        self.running = False

    def run(self):
        if self.running:
            raise RuntimeError("firmware is already running")
        asyncio.run(self._run())

    async def _run(self):
        self.running = True
        # Queue instances
        self.q_control = asyncio.Queue()  # To control the firmware
        self.q_measurements = asyncio.Queue()  # Devices generate measurements
        self.q_actions = asyncio.Queue()  # Devices can receive actions
        self.q_send = asyncio.Queue()  # Messages that need to be sent
        self.q_events = asyncio.Queue()  # Triggered events in the firmware

        # Tasks
        self.core_task = asyncio.create_task(core_task(self))
        self.event_task = asyncio.create_task(events_task(self.q_events, self.q_send))
        self.devices_task = asyncio.create_task(
            devices_task(
                self.q_events, self.q_actions, self.q_measurements, self.q_send
            )
        )
        self.communications_task = asyncio.create_task(
            communications_task(self.q_events, self.q_control, self.q_send)
        )

        logging.info("firmware is running")
        await asyncio.gather(*self.async_tasks)

    @property
    def async_tasks(self):
        return [
            self.core_task,
            self.event_task,
            self.devices_task,
            self.communications_task,
        ]

    def stop(self):
        logging.info("stopping firmware")
        for task in self.async_tasks:
            task.cancel()
        logging.info("firmware has stopped")
