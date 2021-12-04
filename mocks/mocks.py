import asyncio
from typing import Any

from iot_firmware.event import Event
from iot_firmware.event import EventType


class MockEventType(EventType):
    pass


class MockEvent(Event):
    type = MockEventType
    data = 0


async def mock_function(event: MockEvent) -> Any:
    await asyncio.sleep(0.1)
    event.data += 1


class MockObject:
    async def mock_function(self, event: MockEvent) -> Any:
        await asyncio.sleep(0.1)
        event.data += 1
