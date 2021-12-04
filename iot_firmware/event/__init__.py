"""Package that handles all events that happen in the firmware."""
from .handler import EventHandler
from .schema import Event
from .schema import EventType

EventSystem = EventHandler()
