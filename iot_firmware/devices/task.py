import asyncio


async def devices_task(q_events, q_actions, q_measurements, q_send):
    print(q_events, q_actions, q_measurements, q_send)
    await asyncio.sleep(1)
