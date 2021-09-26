import pytest

from iot_firmware.event import CommandEvent
from iot_firmware.event import ReadingEvent
from iot_firmware.event.core import EventHandler
from iot_firmware.event.enum import EventLevel
from mocks.mocks import mock_function
from mocks.mocks import MockEvent


@pytest.fixture(params=[CommandEvent, ReadingEvent])
def event(request):
    return request.param


def test_event_bus_add_subscriber(event):
    event_bus = EventHandler()
    event_bus.add_subscriber(event, mock_function)
    assert event.type.uuid in event_bus.subscribers


def test_event_bus_add_bad_subscriber():
    event_bus = EventHandler()
    with pytest.raises(TypeError):
        event_bus.add_subscriber(MockEvent, None)


def test_event_bus_remove_subscriber():
    event_bus = EventHandler()
    event_bus.add_subscriber(MockEvent, mock_function)
    event_bus.remove_subscriber(MockEvent, mock_function)
    assert MockEvent.type.uuid not in event_bus.subscribers


def test_event_bus_publish_with_subscribers():
    mock_event = MockEvent()
    event_bus = EventHandler()
    event_bus.add_subscriber(MockEvent, mock_function)
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
