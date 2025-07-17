import pytest
from sqlalchemy import text, select
from app.models.task import Task


@pytest.mark.asyncio
async def test_clean_up(session):
    """база вообще жива?"""
    result = await session.execute(text("SELECT 1"))
    one = result.scalar_one_or_none()
    assert one == 1

    result = await session.execute(select(Task))
    res = result.scalars().all()
    assert len(res) == 0
