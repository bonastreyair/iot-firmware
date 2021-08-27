import asyncio


async def communications_task(q_event, q_control, q_send):
    print(q_event, q_control, q_send)
    await asyncio.sleep(1)
