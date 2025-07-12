import pytest_asyncio
from app.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from settings import SQLALCHEMY_TEST_DATABASE_URL

engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL,  poolclass=NullPool)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session")
def _database_url():
    return SQLALCHEMY_TEST_DATABASE_URL

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session():
    async with AsyncSessionLocal() as session:
        yield session
