import uuid
from typing import Any

import pytest

from iot_firmware.event import Event
from iot_firmware.event import EventHandler
from iot_firmware.event import EventType
from iot_firmware.event.enum import EventLevel
from mocks.mocks import mock_function
from mocks.mocks import MockEvent
from mocks.mocks import MockEventType
from mocks.mocks import MockObject


def test_event_handler_subscribe_simple_function():
    event_handler = EventHandler()
    event_handler.subscribe(MockEvent, mock_function)
    assert MockEvent.type.uuid in event_handler.subscribers


def test_event_handler_subscribe_class_function():
    event_handler = EventHandler()
    mock_object = MockObject()
    event_handler.subscribe(MockEvent, mock_object.mock_function)
    assert MockEvent.type.uuid in event_handler.subscribers


def test_event_handler_subscribe_bad_class():
    event_handler = EventHandler()

    class CustomEvent:
        pass

    class Foo:
        def bar(self, event: CustomEvent, what) -> Any:
            pass

    foo = Foo()
    with pytest.raises(TypeError):
        event_handler.subscribe(CustomEvent, foo.bar)


def test_event_handler_subscribe_add_bad_fn():
    event_handler = EventHandler()
    with pytest.raises(TypeError):
        event_handler.subscribe(MockEvent, None)


def test_event_handler_subscribe_add_bad_class_fn():
    event_handler = EventHandler()

    class CustomEvent:
        pass

    with pytest.raises(TypeError):
        event_handler.unsubscribe(CustomEvent, None)


def test_event_handler_unsubscribe_bad_class():
    event_handler = EventHandler()

    class CustomEvent:
        pass

    class Foo:
        def bar(self, event: CustomEvent, what) -> Any:
            pass

    foo = Foo()
    with pytest.raises(TypeError):
        event_handler.subscribe(CustomEvent, foo.bar)


def test_event_handler_unsubscribe_add_bad_fn():
    event_handler = EventHandler()
    with pytest.raises(TypeError):
        event_handler.unsubscribe(MockEvent, None)


def test_event_handler_unsubscribe_add_bad_class_fn():
    event_handler = EventHandler()

    class CustomEvent:
        pass

    with pytest.raises(TypeError) as exc_info:
        event_handler.unsubscribe(CustomEvent, None)

    assert len(exc_info.value.args) == 2


def test_event_handler_unsubscribe():
    event_handler = EventHandler()
    event_handler.subscribe(MockEvent, mock_function)
    event_handler.unsubscribe(MockEvent, mock_function)
    assert MockEvent.type.uuid not in event_handler.subscribers


def test_event_handler_publish_with_subscribers():
    mock_event = MockEvent()
    event_handler = EventHandler()
    event_handler.subscribe(MockEvent, mock_function)
    event_handler.publish(mock_event)


def test_event_handler_publish_no_event():
    class CustomEvent:
        pass

    mock_event = CustomEvent()
    event_handler = EventHandler()
    with pytest.raises(TypeError):
        event_handler.publish(mock_event)


def test_event_handler_publish_without_subscribers():
    mock_event = MockEvent()
    event_handler = EventHandler()
    event_handler.publish(mock_event)


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


def test_event_data():
    mock_event = MockEvent(data="test")
    assert mock_event.data == "test"


def test_print_event():
    mock_event = MockEvent()
    assert mock_event.__repr__() == "MockEvent(data=None, level='INFO')"


def test_print_event_type():
    mock_event_type = MockEventType()
    assert mock_event_type.__repr__() == "MockEventType()"


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
        type: EventType = MockEventType

    foo = FooEvent()

    assert FooEvent.type.uuid is foo.type.uuid
    assert isinstance(foo.uuid, str)
    assert isinstance(foo.timestamp, float)

    new_foo = FooEvent()

    assert new_foo.uuid != foo.uuid

    class BarEvent(Event):
        type: EventType = MockEventType

    bar = BarEvent()

    assert foo.uuid != bar.uuid
