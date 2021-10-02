from iot_firmware.event import Event
from iot_firmware.event import EventType


class MockEventType(EventType):
    name: str = "mock_event_type"


class MockEvent(Event):
    name: str = "mock_event"
    type: EventType = MockEventType


def mock_function(event: MockEvent):
    pass
