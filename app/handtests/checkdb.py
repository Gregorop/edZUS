import asyncio

from app.core.database import engine

async def test_connection():
    async with engine.connect() as conn:
        print("Подключение к PostgreSQL успешно!")
    await engine.dispose()

asyncio.run(test_connection())
