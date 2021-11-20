from typing import Any

from iot_firmware.event import Event
from iot_firmware.event import EventType


class MockEventType(EventType):
    pass


class MockEvent(Event):
    type = MockEventType


def mock_function(event: MockEvent) -> Any:
    pass
