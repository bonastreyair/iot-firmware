import asyncio


async def core_task(fw):
    print(fw)
    await asyncio.sleep(1)
