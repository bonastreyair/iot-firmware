import uuid

import pytest

from iot_firmware.event import Event
from iot_firmware.event import EventHandler
from iot_firmware.event import EventType
from iot_firmware.event.basic import CommandEvent
from iot_firmware.event.basic import ReadingEvent
from iot_firmware.event.enum import EventLevel
from mocks.mocks import mock_function
from mocks.mocks import MockEvent
from mocks.mocks import MockEventType


@pytest.fixture(params=[CommandEvent, ReadingEvent])
def event(request):
    return request.param


def test_event_bus_add_subscriber(event):
    event_bus = EventHandler()
    event_bus.subscribe(event, mock_function)
    assert event.type.uuid in event_bus.subscribers


def test_event_bus_add_bad_subscriber():
    event_bus = EventHandler()
    with pytest.raises(TypeError):
        event_bus.subscribe(MockEvent, None)


def test_event_bus_remove_subscriber():
    event_bus = EventHandler()
    event_bus.subscribe(MockEvent, mock_function)
    event_bus.unsubscribe(MockEvent, mock_function)
    assert MockEvent.type.uuid not in event_bus.subscribers


def test_event_bus_publish_with_subscribers():
    mock_event = MockEvent()
    event_bus = EventHandler()
    event_bus.subscribe(MockEvent, mock_function)
    event_bus.publish(mock_event)


def test_event_bus_publish_without_subscribers():
    mock_event = MockEvent()
    event_bus = EventHandler()
    event_bus.publish(mock_event)


def test_event_uuid():
    mock_event_a = MockEvent()
    mock_event_b = MockEvent()
    assert mock_event_a.uuid != mock_event_b.uuid
    assert mock_event_a.type.uuid == mock_event_b.type.uuid


def test_event_level():
    mock_event_a = MockEvent()
    assert mock_event_a.level == EventLevel.INFO
    mock_event_b = MockEvent(level=EventLevel.ERROR)
    assert mock_event_b.level == EventLevel.ERROR


def test_event_name():
    mock_event = MockEvent()
    assert mock_event.name == "mock_event"


def test_event_type_name():
    mock_event = MockEvent()
    assert mock_event.type.name == "mock_event_type"


def test_event_data():
    mock_event = MockEvent(data="test")
    assert mock_event.data == "test"


def test_print_event():
    mock_event = MockEvent()
    print(mock_event)


def test_print_event_type():
    mock_event = MockEvent()
    print(mock_event.type)


def test_event_type_class():
    class FooEventType(EventType):
        name: str = "foo_event_type"

    assert FooEventType.name == "foo_event_type"
    assert isinstance(FooEventType.uuid, str)
    assert FooEventType.uuid != ""
    assert len(FooEventType.uuid) == len(str(uuid.uuid4()))

    class BarEventType(EventType):
        name: str = "bar_event_type"

    assert FooEventType.uuid != BarEventType.uuid


def test_event_class():
    class FooEvent(Event):
        name: str = "foo_event"
        type: EventType = MockEventType

    foo = FooEvent()

    assert FooEvent.type.uuid is foo.type.uuid
    assert FooEvent.name is foo.name
    assert FooEvent.name == "foo_event"
    assert isinstance(foo.uuid, str)
    assert isinstance(foo.timestamp, float)

    new_foo = FooEvent()

    assert new_foo.uuid != foo.uuid

    class BarEvent(Event):
        name: str = "bar_event"
        type: EventType = MockEventType

    bar = BarEvent()

    assert foo.uuid != bar.uuid
