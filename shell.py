import asyncio
from app.core.database import engine, AsyncSessionLocal
from aioconsole import interact

async def async_shell():
    session = AsyncSessionLocal()
    
    async def wrapper():
        globals().update({'session': session, 'engine': engine})
        await interact()
    
    try:
        await wrapper()
    finally:
        await session.close()
        await engine.dispose()

asyncio.run(async_shell())
