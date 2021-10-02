import abc
import uuid


class EventTypeMeta(abc.ABCMeta, type):
    """Meta class for event types.
    It generates a uuid for each unique event type class."""

    def __init__(cls, what, bases, dct):
        super().__init__(what, bases, dct)
        cls.uuid: str = str(uuid.uuid4())


class EventType(metaclass=EventTypeMeta):
    """Abstract class for eny Event type class."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the Event Type."""
