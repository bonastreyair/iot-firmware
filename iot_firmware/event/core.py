import asyncio
import logging
import time
import uuid
from abc import ABC
from collections import defaultdict
from typing import Any
from typing import Callable
from typing import Dict
from typing import Type

from ..enums import TIME_FORMAT
from .enum import EventLevel


class EventType:
    uuid: str = str(uuid.uuid4())

    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return self.name


class Event(ABC):
    type: EventType

    def __init__(
        self, name: str, level: EventLevel = EventLevel.INFO, data: Any = None
    ):
        self.__name = name
        self.__level = level
        self.__data = data
        self.__uuid = str(uuid.uuid4())
        self.__timestamp = time.time()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def level(self) -> EventLevel:
        return self.__level

    @property
    def data(self) -> Any:
        return self.__data

    @property
    def uuid(self) -> str:
        return self.__uuid

    @property
    def timestamp(self) -> float:
        return self.__timestamp

    def __repr__(self) -> str:
        time_format = time.strftime(TIME_FORMAT, time.gmtime(self.timestamp))
        return f"{self.level.name}: {time_format} [{self.name} {self.type.name} EVENT]: {self.data}"


class EventHandler:
    def __init__(self) -> None:
        self.__subscribers: Dict[str, set] = defaultdict(set)

    @property
    def subscribers(self) -> Dict[str, set]:
        return self.__subscribers

    def add_subscriber(self, event_type: Type[Event], fn: Callable) -> None:
        if not isinstance(fn, Callable):
            raise TypeError(f"function {fn} is not Callable")
        self.__subscribers[event_type.type.uuid].add(fn)

    def remove_subscriber(self, event_type: Type[Event], fn: Callable) -> None:
        self.__subscribers[event_type.type.uuid].remove(fn)
        if len(self.__subscribers[event_type.type.uuid]) == 0:
            del self.__subscribers[event_type.type.uuid]

    def publish(self, event: Event):
        logging.debug(event)
        if event.type.uuid not in self.__subscribers:
            return

        for fn in self.__subscribers[event.type.uuid]:
            fn(event)
            logging.debug(
                f"execution_latency since event: {time.time() - event.timestamp}s"
            )


# class AsyncEventBus(EventBus):
#     def add_subscriber(self, event: Event, fn: Callable) -> None:
#         if not asyncio.iscoroutinefunction(fn):
#             logging.error(f"function {fn} is not a coroutine")
#             return
#         super().add_subscriber(event, fn)
#
#     async def publish(self, event: Event):
#         logging.debug(event)
#         if event.type not in self.__subscribers:
#             return
#
#         for fn in self.__subscribers[event.uuid]:
#             await fn(event)
#             logging.debug(
#                 f"execution_latency since event: {time.time() - event.timestamp}s"
#             )
