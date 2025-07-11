import asyncio

from app.core.database import engine

async def check_connection():
    '''ручками запустить проверить видит ли контейнер постгреса'''
    async with engine.connect() as conn:
        print("Подключение к PostgreSQL успешно!")
    await engine.dispose()

asyncio.run(check_connection())
