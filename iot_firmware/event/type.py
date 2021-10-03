import abc
import uuid


class EventTypeMeta(abc.ABCMeta, type):
    """Meta class for event types.

    It generates a uuid for each unique event type class.
    """

    def __init__(cls, what, bases, dct) -> None:
        super().__init__(what, bases, dct)
        cls.uuid: str = str(uuid.uuid4())


class EventType(abc.ABC, metaclass=EventTypeMeta):
    """Abstract class for any Event type class."""

    name: str
    uuid: str

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the Event Type."""
