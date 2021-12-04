import asyncio
import logging
from typing import Dict
from typing import List

import uvloop

from .communications import CommunicationsHandler
from .event import EventHandler
from .schema import read_config


class Controller:
    """Firmware main controller.

    :param config: configuration for the controller
    """

    def __init__(self, config: Dict = None) -> None:
        uvloop.install()
        self.config = read_config(config)

        self.event_handler = EventHandler()
        self.communications_handler = CommunicationsHandler()

        self.firmware_async_task = None

        self.running = False

    def start(self) -> None:
        """Starts the firmware."""
        if self.running:
            raise RuntimeError("firmware is already running")
        self.running = True
        asyncio.run(self.start_async())

    async def start_async(self) -> None:
        """Async function to start the async tasks."""
        self.firmware_async_task = asyncio.create_task(self.firmware_async())
        logging.info("firmware is running")
        await asyncio.gather(*self.async_tasks)

    @property
    def async_tasks(self) -> List:
        return [self.firmware_async_task]

    def stop(self) -> None:
        """Stops the firmware."""
        logging.info("stopping firmware")
        for task in self.async_tasks:
            task.cancel()
        logging.info("firmware has stopped")

    async def firmware_async(self) -> None:
        await asyncio.sleep(1)
