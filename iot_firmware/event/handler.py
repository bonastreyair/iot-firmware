"""Module in charge of handling function event subscriptions."""
import asyncio
import inspect
import logging
import time
from asyncio import queues
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Type

from ..enums import NameClassMeta
from .enum import EventHandlerState
from .schema import Event

logger = logging.getLogger(__name__)

DEFAULT_NUM_WORKERS = 10
DEFAULT_BUFFER_MAXSIZE = 100
DEFAULT_WORKER_TIMEOUT_SECONDS = 2


@dataclass
class EventHandler:
    """Class that handles Events.

    It is in charge to execute all subscribed functions to an Event.

    Basic usage.

    >>> event_handler = EventHandler()
    >>> event_handler.state.name
    'IDLE'
    """

    num_workers: int = field(default=DEFAULT_NUM_WORKERS)
    buffer_maxsize: int = field(repr=False, default=DEFAULT_BUFFER_MAXSIZE)
    worker_timeout_seconds: float = field(
        repr=False, default=DEFAULT_WORKER_TIMEOUT_SECONDS
    )

    state: EventHandlerState = field(repr=False, default=EventHandlerState.IDLE)

    _subscribers: Dict[str, set] = field(
        init=False, repr=False, default_factory=lambda: defaultdict(set)
    )
    _workers: List = field(init=False, repr=False, default_factory=list)
    _event_buffer: queues.Queue = field(init=False, repr=False)

    def __post_init__(self):
        """Initialize missing objects after the __init__."""
        self._event_buffer = queues.Queue(maxsize=self.buffer_maxsize)
        logger.debug(self.state.name)

    def subscribe(self, event_class: Type[Event], fn: Callable) -> None:
        """Subscribes a function to an EventType.

        :param event_class: event class that contains an event type
        :param fn: function that is going to be called with the event object
        """
        self._check_types(event_class, fn)
        self._subscribers[event_class.type.uuid].add(fn)
        logger.debug(
            f"subscribed async function `{fn.__name__}` "
            f"after every `{event_class.type.__name__}` event"
        )

    def unsubscribe(self, event_class: Type[Event], fn: Callable) -> None:
        """Unsubscribes a function to an EventType.

        :param event_class: event class that contains an event type
        :param fn: function that is going to be called with the event object
        """
        self._check_types(event_class, fn)
        if event_class.type.uuid not in self._subscribers:
            logger.error(f"event type {event_class.type.__name__} was never subscribed")
            return

        self._subscribers[event_class.type.uuid].remove(fn)
        logger.debug(
            f"unsubscribed {fn.__name__} after every `{event_class.type.__name__}` event"
        )

        if len(self._subscribers[event_class.type.uuid]) == 0:
            del self._subscribers[event_class.type.uuid]
            logger.warning(
                f"event {event_class.type.__name__} will not trigger any function"
            )

    def publish(self, event: Event) -> None:
        """Adds the event into a queue buffer to be processed.

        :param event: standard event inherited from Event class
        """
        if self._discard_event(event):
            return

        if self.state is EventHandlerState.IDLE:
            logger.warning(
                f"handler is in {self.state.name} state, but it will be stored in the buffer"
            )

        logger.debug(f"event `{event}` was published")
        if self._event_buffer.full():
            logger.warning(f"buffer is full (events:{self._event_buffer.qsize()})")
            self._discard_oldest_event()

        self._event_buffer.put_nowait((event, time.time()))
        logger.debug(f"event `{event}` is the buffer, pending to be executed")

    async def run(self):
        """Main function that starts workers to handle event requests."""
        self._workers = [
            asyncio.create_task(self._worker(i), name=f"worker_{i}")
            for i in range(self.num_workers)
        ]
        self.state = EventHandlerState.RUNNING
        logger.info(self.state.name)
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers = []
        self.state = EventHandlerState.IDLE
        logger.debug(self.state.name)

    async def stop(self) -> None:
        """Send poison pills to all workers."""
        if self.state is not EventHandlerState.RUNNING:
            raise RuntimeError("event handler is not running")
        self.state = EventHandlerState.STOPPING
        logger.debug(self.state.name)
        for _ in self._workers:
            await self._event_buffer.put((PoisonPill, time.time()))

    def cancel(self) -> None:
        """Cancels all workers."""
        if self.state is not EventHandlerState.RUNNING:
            raise RuntimeError("event handler is not running")
        logger.debug("cancelling all workers")
        for worker in self._workers:
            worker.cancel()
        logger.debug("cancelled all workers")

    async def _worker(self, i: int) -> None:
        """Calls all subscribed functions with the same event type.

        :param i: unique id number of the worker
        """
        event = await self._get_next_event()
        while event is not PoisonPill:
            tasks = [
                asyncio.create_task(fn(event), name=fn.__name__)
                for fn in self._subscribers[event.type.uuid]
            ]
            try:
                await asyncio.wait_for(
                    self._run_tasks(tasks, event), timeout=self.worker_timeout_seconds
                )
            except asyncio.TimeoutError:
                logger.error(
                    f"exceeded max computation time of {self.worker_timeout_seconds}s for `{event}`"
                )
            t = time.time()
            logger.debug(f"worker {i} processing latency: {t - event.timestamp:.3f}s")
            event = await self._get_next_event()
        logger.info(f"worker {i} stopped")

    @staticmethod
    async def _run_tasks(tasks: List, event: Event) -> None:
        """Function that runs various tasks with the event.

        It is in charge of scheduling them in the async event loop.
        It also captures and logs any errors that might appear during their executions.

        :param tasks: list of async tasks that are going to be executed
        :param event: standard event inherited from Event class
        """
        logger.debug(
            f"awaiting for {[task.get_name() for task in tasks]} triggered by `{event}`"
        )
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:
            cancelled_tasks = [task for task in tasks if task.cancelled()]
            logger.warning(f"gather cancelled {len(cancelled_tasks)} task(s)")

        for task in tasks:
            if task.cancelled():
                logger.warning(f"task `{task.get_name()}` was cancelled")
            if not task.cancelled() and task.exception():
                logger.error(
                    f"error captured in `{task.get_coro().__name__}` after `{event}` "
                    f"- {task.exception().__class__.__name__}: {task.exception()}"
                )

    def _discard_oldest_event(self) -> None:
        """Discards the oldest event in the event buffer."""
        event, entered_in_buffer = self._event_buffer.get_nowait()
        t = time.time()
        logger.error(
            f"event `{event}` was discarded "
            f"(in buffer time {t - entered_in_buffer:.3f}s)"
        )

    async def _get_next_event(self) -> Event:
        """Gets next event from the event buffer.

        It also logs the amount of time the event has been waiting in
        the buffer.
        """
        event, entered_in_buffer = await self._event_buffer.get()
        t = time.time()
        logger.debug(
            f"event `{event}` has been in buffer for {t - entered_in_buffer:.3f}s"
        )
        return event

    @staticmethod
    def _check_types(event_class: Type[Event], fn: Callable) -> None:
        """Checks types and raises a TypeError if not correct.

        :param event_class: standard event class inherited from Event class
        """
        errors = []
        if not issubclass(event_class, Event):
            errors.append(f"event class {event_class} is not subclassed from Event")
        if not isinstance(fn, Callable):
            errors.append(f"function {fn} is not Callable")
        if not inspect.iscoroutinefunction(fn):
            errors.append(f"function {fn} is not async")
        if errors:
            raise TypeError(*errors)

    def _discard_event(self, event: Any) -> bool:
        """Checks whether the event must be discarded or not.

        :param event: standard event inherited from Event class
        """
        if not isinstance(event, Event):
            logger.error(f"discarded event `{event}` -> not subclassed from Event")
            return True
        if event.type.uuid not in self._subscribers:
            logger.debug(f"discarded event `{event}` -> there were no subscribers")
            return True
        if self.state is EventHandlerState.STOPPING:
            logger.warning(f"discarded event `{event}` -> state is {self.state.name}")
            return True

        return False


class PoisonPill(metaclass=NameClassMeta):
    """Poison pill used to stop the workers gracefully."""
