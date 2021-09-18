import asyncio
from enum import Enum


async def event_task(q_event, q_send):
    await asyncio.sleep(1)


class EventTypes(Enum):
    THRESHOLD = "threshold"

    WARNING = "warning"
    ERROR = "error"
