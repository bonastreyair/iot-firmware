import asyncio
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
    assert MockEvent.type.uuid in event_handler._subscribers


def test_event_handler_subscribe_class_function():
    event_handler = EventHandler()
    mock_object = MockObject()
    event_handler.subscribe(MockEvent, mock_object.mock_function)
    assert MockEvent.type.uuid in event_handler._subscribers


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

    assert exc_info.value.args


def test_event_handler_unsubscribe():
    event_handler = EventHandler()
    event_handler.subscribe(MockEvent, mock_function)
    event_handler.unsubscribe(MockEvent, mock_function)
    assert MockEvent.type.uuid not in event_handler._subscribers


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
    event_handler.publish(mock_event)
    assert event_handler._event_buffer.qsize() == 0


def test_event_handler_publish_no_event_with_subscriber():
    class CustomEvent:
        pass

    mock_event = CustomEvent()
    event_handler = EventHandler()
    event_handler.subscribe(MockEvent, mock_function)
    event_handler.publish(mock_event)
    assert event_handler._event_buffer.qsize() == 0


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


def test_unsubscribe_a_not_subscribed_event():
    event_handler = EventHandler()
    event_handler.unsubscribe(MockEvent, mock_function)


def test_event_handler_is_full():
    event_handler = EventHandler(buffer_maxsize=2)
    assert not event_handler._event_buffer.full()

    event_handler.subscribe(MockEvent, mock_function)
    event_handler.publish(MockEvent())
    assert not event_handler._event_buffer.full()

    event_handler.publish(MockEvent())
    assert event_handler._event_buffer.full()

    event_handler.publish(MockEvent())
    assert event_handler._event_buffer.full()


@pytest.mark.asyncio
async def test_event_handler_worker_workflow_function():
    event_handler = EventHandler(buffer_maxsize=2, num_workers=1)
    event_handler.subscribe(MockEvent, mock_function)

    event = MockEvent(data=0)
    event_handler.publish(event)

    try:
        await asyncio.wait_for(event_handler.run(), timeout=0.3)
    except asyncio.TimeoutError:
        pass

    assert event.data == 1


@pytest.mark.asyncio
async def test_event_handler_worker_timeout():
    event_handler = EventHandler(
        buffer_maxsize=2, num_workers=1, worker_timeout_seconds=0.5
    )

    async def quick_function(event: MockEvent):
        await asyncio.sleep(0.1)
        event.data += 1

    async def slow_function(event: MockEvent):
        await asyncio.sleep(1)
        event.data += 1

    event_handler.subscribe(MockEvent, quick_function)
    event_handler.subscribe(MockEvent, slow_function)

    mock_event = MockEvent(data=0)
    event_handler.publish(mock_event)

    try:
        await asyncio.wait_for(event_handler.run(), timeout=1)
    except asyncio.TimeoutError:
        pass

    assert mock_event.data == 1


@pytest.mark.asyncio
async def test_event_handler_stop_workers():
    event_handler = EventHandler(num_workers=2)

    async def normal_function(event: MockEvent):
        await asyncio.sleep(0.5)
        event.data += 1

    event_handler.subscribe(MockEvent, normal_function)

    mock_event = MockEvent(data=0)
    event_handler.publish(mock_event)

    async def stop_event_handler(event_handler_local: EventHandler):
        await asyncio.sleep(0.2)
        await event_handler_local.stop()

    await asyncio.gather(event_handler.run(), stop_event_handler(event_handler))

    assert mock_event.data == 1
    assert len(event_handler._workers) == 0


@pytest.mark.asyncio
async def test_event_handler_stopping_workers():
    event_handler = EventHandler(num_workers=1, buffer_maxsize=1)

    async def normal_function(event: MockEvent):
        await asyncio.sleep(0.5)
        event.data += 1

    event_handler.subscribe(MockEvent, normal_function)

    mock_event = MockEvent(data=0)
    event_handler.publish(mock_event)

    async def stop_event_handler(event_handler_local: EventHandler):
        await asyncio.sleep(0.2)
        await event_handler_local.stop()
        event_handler.publish(mock_event)
        await asyncio.sleep(1)
        event_handler.publish(mock_event)

    await asyncio.gather(event_handler.run(), stop_event_handler(event_handler))

    assert mock_event.data == 1
    assert len(event_handler._workers) == 0


@pytest.mark.asyncio
async def test_event_handler_stop_workers_error():
    event_handler = EventHandler()

    with pytest.raises(RuntimeError):
        await event_handler.stop()


@pytest.mark.asyncio
async def test_event_handler_cancel_workers():
    event_handler = EventHandler(num_workers=2)

    async def normal_function(event: MockEvent):
        await asyncio.sleep(0.5)
        event.data += 1

    event_handler.subscribe(MockEvent, normal_function)

    mock_event = MockEvent(data=0)
    event_handler.publish(mock_event)

    async def cancel_event_handler(event_handler_local: EventHandler):
        await asyncio.sleep(0.2)
        event_handler_local.cancel()

    await asyncio.gather(event_handler.run(), cancel_event_handler(event_handler))

    assert mock_event.data == 0
    assert len(event_handler._workers) == 0


def test_event_handler_cancel_workers_error():
    event_handler = EventHandler()

    with pytest.raises(RuntimeError):
        event_handler.cancel()


@pytest.mark.asyncio
async def test_event_handler_raise_error_in_function():
    event_handler = EventHandler(num_workers=2)

    async def function_raise_error(event: MockEvent):
        raise RuntimeError("error triggered")

    event_handler.subscribe(MockEvent, function_raise_error)

    mock_event = MockEvent(data=0)
    event_handler.publish(mock_event)

    try:
        await asyncio.wait_for(event_handler.run(), timeout=0.5)
    except asyncio.TimeoutError:
        pass
