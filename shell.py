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
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    aliased,
    load_only,
    sessionmaker,
)

from app.models.base import DBTask
from settings import LOCAL_SQLALCHEMY_DATABASE_URL

engine = create_async_engine(LOCAL_SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def async_shell():
    session = AsyncSessionLocal()

    namespace = {
        "session": session,
        "DBTask": DBTask,
        "select": select,
        "insert": insert,
        "update": update,
        "delete": delete,
        "and_": and_,
        "or_": or_,
        "not_": not_,
        "text": text,
        "asc": asc,
        "desc": desc,
        "load_only": load_only,
        "aliased": aliased,
    }

    async def wrapper():
        await interact(banner="мой shell c awaitom и моделями", locals=namespace)

    try:
        await wrapper()
    finally:
        await session.close()
        await engine.dispose()


asyncio.run(async_shell())
