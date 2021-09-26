from iot_firmware.event.core import Event
from iot_firmware.event.core import EventType


class MockEvent(Event):
    type: EventType = EventType("mock_event_type")

    def __init__(self, *args, **kwargs):
        super().__init__(name="mock_event", *args, **kwargs)


def mock_function(event: MockEvent):
    pass
