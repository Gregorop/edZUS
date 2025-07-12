import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import quoted_name

from app.models.base import Base
from settings import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_TEST_DATABASE_URL, TEST_DB_NAME

engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL,  poolclass=NullPool)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session")
def _database_url():
    return SQLALCHEMY_TEST_DATABASE_URL

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    admin_engine = create_async_engine(SQLALCHEMY_DATABASE_URL,isolation_level="AUTOCOMMIT")
    safe_db_name = quoted_name(TEST_DB_NAME, quote=True)
    async with admin_engine.begin() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {safe_db_name}"))
        await conn.execute(text(f"CREATE DATABASE {safe_db_name}"))

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with admin_engine.begin() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {safe_db_name}"))


@pytest_asyncio.fixture
async def session():
    async with AsyncSessionLocal() as session:
        yield session
