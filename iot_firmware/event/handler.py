"""Module in charge of handling function event subscriptions."""
import logging
import time
from collections import defaultdict
from typing import Any
from typing import Callable
from typing import Dict
from typing import Type

from .schema import Event


class EventHandler:
    """Class that handles Events.

    It is in charge to execute all subscribed functions to an Event.

    Basic usage.

    >>> event_handler = EventHandler()
    >>> event_handler.subscribers
    defaultdict(<class 'set'>, {})
    """

    subscribers: Dict[str, set]

    def __init__(self) -> None:
        self.__subscribers = defaultdict(set)

    @property
    def subscribers(self) -> Dict[str, set]:
        """Returns the dict of all the subscribers."""
        return self.__subscribers

    def subscribe(self, event_class: Type[Event], fn: Callable[[Event], Any]) -> None:
        """Subscribes a function to an EventType.

        :param event_class: event class that contains an event type
        :param fn: function that is going to be called with the event object
        """
        if not isinstance(fn, Callable):
            raise TypeError(f"function {fn} is not Callable")
        self.__subscribers[event_class.type.uuid].add(fn)

    def unsubscribe(self, event_class: Type[Event], fn: Callable[[Event], Any]) -> None:
        """Unsubscribes a function to an EventType.

        :param event_class: event class that contains an event type
        :param fn: function that is going to be called with the event object
        """
        if event_class.type.uuid not in self.__subscribers:
            logging.error(f"event type {event_class.type.name} was never subscribed")
            return

        self.__subscribers[event_class.type.uuid].remove(fn)

        if len(self.__subscribers[event_class.type.uuid]) == 0:
            del self.__subscribers[event_class.type.uuid]

    def publish(self, event: Event) -> None:
        """Calls all subscribed functions with the same event type.

        :param event: standard event inherited from Event class
        """
        logging.debug(event)
        if event.type.uuid not in self.__subscribers:
            return

        for fn in self.__subscribers[event.type.uuid]:
            fn(event)
            logging.debug(
                f"{event} execution latency: {time.time() - event.timestamp}s"
            )
