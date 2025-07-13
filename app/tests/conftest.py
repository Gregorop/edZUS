import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.models.base import Base
from settings import SQLALCHEMY_DATABASE_URL

load_dotenv()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session")
def _database_url():
    return SQLALCHEMY_DATABASE_URL


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def session():
    async with AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(base_url="http://api_test:8000") as client:
        yield client
