import asyncio


async def monitor_task(q_event, q_send):
    print(q_event, q_send)
    await asyncio.sleep(1)
