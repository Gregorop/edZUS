import asyncio

from aioconsole import interact
from sqlalchemy import (
    and_,
    asc,
    delete,
    desc,
    insert,
    not_,
    or_,
    select,
    text,
    update,
)
from sqlalchemy.orm import (
    aliased,
    load_only,
)

from app.core.database import AsyncSessionLocal, engine
from app.models.base import DBTask


async def async_shell():
    session = AsyncSessionLocal()
    
    namespace = {
        'session': session,
        'DBTask': DBTask,
        
        'select': select,
        'insert': insert,
        'update': update,
        'delete': delete,
        
        'and_': and_,
        'or_': or_,
        'not_': not_,
        'text': text,
        'asc': asc,
        'desc': desc,

        'load_only': load_only,
        'aliased': aliased,
    }

    async def wrapper():
        await interact(banner="мой shell c awaitom и моделями",locals=namespace)
    
    try:
        await wrapper()
    finally:
        await session.close()
        await engine.dispose()

asyncio.run(async_shell())
