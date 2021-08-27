import asyncio


async def events_task(q_event, q_send):
    print(q_event, q_send)
    await asyncio.sleep(1)
