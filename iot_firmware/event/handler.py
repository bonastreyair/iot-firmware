import logging
import time
from collections import defaultdict
from typing import Callable
from typing import Dict
from typing import Type

from .event import Event


class EventHandler:
    def __init__(self) -> None:
        self.__subscribers: Dict[str, set] = defaultdict(set)

    @property
    def subscribers(self) -> Dict[str, set]:
        """Returns the dict of all the subscribers."""
        return self.__subscribers

    def subscribe(self, event: Type[Event], fn: Callable) -> None:
        """Subscribes a function to an EventType to be handled by the
        EventHandler."""
        if not isinstance(fn, Callable):
            raise TypeError(f"function {fn} is not Callable")
        self.__subscribers[event.type.uuid].add(fn)

    def unsubscribe(self, event: Type[Event], fn: Callable) -> None:
        """Unsubscribe a function to an EventType to be handled by the
        EventHandler."""
        if event.type.uuid not in self.__subscribers:
            logging.error(f"event type {event.type.name} was never subscribed")
            return

        self.__subscribers[event.type.uuid].remove(fn)

        if len(self.__subscribers[event.type.uuid]) == 0:
            del self.__subscribers[event.type.uuid]

    def publish(self, event: Event):
        logging.debug(event)
        if event.type.uuid not in self.__subscribers:
            return

        for fn in self.__subscribers[event.type.uuid]:
            fn(event)
            logging.debug(f"execution_latency: {time.time() - event.timestamp}s")
