"""Module in charge of handling function event subscriptions."""
import asyncio
import logging
import time
from asyncio import queues
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import Dict
from typing import List
from typing import Type

from .schema import Event

logger = logging.getLogger(__name__)

MAX_BUFFERED_EVENTS = 100
WORKER_TIMEOUT_SECONDS = 5


@dataclass
class EventHandler:
    """Class that handles Events.

    It is in charge to execute all subscribed functions to an Event.

    Basic usage.

    >>> event_handler = EventHandler()
    >>> event_handler.subscribers
    defaultdict(<class 'set'>, {})
    """

    num_workers: int = field(init=True, repr=True, default=4)
    worker_timeout_seconds: float = field(
        init=True, repr=False, default=WORKER_TIMEOUT_SECONDS
    )
    buffer_maxsize: int = field(init=True, repr=False, default=WORKER_TIMEOUT_SECONDS)

    subscribers: Dict[str, set] = field(
        init=False, repr=True, default_factory=lambda: defaultdict(set)
    )
    event_buffer: queues.Queue = field(init=False, repr=False)
    workers: List = field(init=False, repr=False, default_factory=list)

    def __post_init__(self):
        """Initialize missing objects after the __init__."""
        self.event_buffer = queues.Queue(maxsize=self.buffer_maxsize)

    def subscribe(self, event_class: Type[Event], fn: Callable) -> None:
        """Subscribes a function to an EventType.

        :param event_class: event class that contains an event type
        :param fn: function that is going to be called with the event object
        """
        self._check_types(event_class, fn)
        self.subscribers[event_class.type.uuid].add(fn)
        logger.debug(
            f"function {fn} will be called after every {event_class.type} event"
        )

    def unsubscribe(self, event_class: Type[Event], fn: Callable) -> None:
        """Unsubscribes a function to an EventType.

        :param event_class: event class that contains an event type
        :param fn: function that is going to be called with the event object
        """
        self._check_types(event_class, fn)
        if event_class.type.uuid not in self.subscribers:
            logger.error(f"event type {event_class.type} was never subscribed")
            return

        self.subscribers[event_class.type.uuid].remove(fn)
        logger.debug(f"event {event_class.type} will no longer trigger function: {fn}")

        if len(self.subscribers[event_class.type.uuid]) == 0:
            del self.subscribers[event_class.type.uuid]
            logger.warning(f"event {event_class.type} will not trigger any function")

    def publish(self, event: Event) -> None:
        """Adds the event into a queue buffer to be processed.

        :param event: standard event inherited from Event class
        """
        if not isinstance(event, Event):
            raise TypeError(f"event {event} is not subclassed from Event")

        logger.debug(f"event {event} was published")
        if event.type.uuid not in self.subscribers:
            return

        if self.event_buffer.full():
            logger.error("event_buffer is full")
            event = self.get_next_event_nowait()

        self.event_buffer.put_nowait((event, time.time()))
        logger.debug(f"event {event} is pending to be executed")

    async def worker(self, i) -> None:
        """Calls all subscribed functions with the same event type."""
        while event := await self.get_next_event():
            tasks = [
                asyncio.create_task(fn(event), name=fn.__name__)
                for fn in self.subscribers[event.type.uuid]
            ]

            try:
                logger.debug(f"processing {len(tasks)} tasks")
                await asyncio.wait_for(
                    self.run_tasks(tasks, event), timeout=WORKER_TIMEOUT_SECONDS
                )
            except asyncio.TimeoutError:
                logger.error(
                    f"exceeded max event {event} computation time of {WORKER_TIMEOUT_SECONDS}s"
                )
            t = time.time()
            logger.debug(f"{event} execution latency: {t - event.timestamp}s)")
            for task in tasks:
                if task.cancelled():
                    logger.debug(
                        f"task {task.get_name()} was cancelled since it lasted more than 3 seconds"
                    )
        logger.info(f"worker {i} has stopped after a poison pill")

    @staticmethod
    async def run_tasks(tasks: List, event: Event) -> None:
        logger.info(f"awaiting for {len(tasks)} tasks")
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:
            cancelled_tasks = [task for task in tasks if task.cancelled()]
            logger.warning(f"gather cancelled {len(cancelled_tasks)} task(s)")

        for task in tasks:
            if not task.cancelled and task.exception():
                logger.error(
                    f"error during task {task.get_coro()} after {event} event "
                    f"- {task.exception().__class__.__name__}: {task.exception()}"
                )

    def get_next_event_nowait(self) -> Event:
        event, entered_in_buffer = self.event_buffer.get_nowait()
        t = time.time()
        logger.error(
            f"event {event} was lost (in buffer time {t - entered_in_buffer:.3f}s)"
        )
        return event

    async def get_next_event(self) -> Event:
        event, entered_in_buffer = await self.event_buffer.get()
        t = time.time()
        logger.debug(f"time in buffer {t - entered_in_buffer}")
        return event

    async def run(self):
        self.workers = [
            asyncio.create_task(self.worker(i), name=f"worker_{i}")
            for i in range(self.num_workers)
        ]
        logger.info(f"running {self.__name__}")
        try:
            await asyncio.gather(*self.workers)
        except asyncio.CancelledError:
            logger.debug("workers were cancelled")
        logger.info(f"finished {self.__name__}")

    async def stop(self) -> None:
        """Send poison pills to all workers."""
        logger.debug("stopping all workers")
        for _ in self.workers:
            await self.event_buffer.put(None)
        logger.debug("stopped all workers")

    async def cancel(self) -> None:
        """Cancels all workers."""
        logger.debug("cancelling all workers")
        for worker in self.workers:
            worker.cancel()
        logger.debug("cancelled all workers")

    @staticmethod
    def _check_types(event_class: Type[Event], fn: Callable) -> None:
        """Checks types and raises a TypeError if not correct."""
        errors = []
        if not issubclass(event_class, Event):
            errors.append(f"event class {event_class} is not subclassed from Event")
        if not isinstance(fn, Callable):
            errors.append(f"function {fn} is not Callable")
        if errors:
            raise TypeError(*errors)
