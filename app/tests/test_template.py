import pytest
from sqlalchemy import select, func

from app.models.base import DBTask
from app.models.task import Task
from app.models.templates import FooTemplate


@pytest.mark.asyncio
async def test_task_create(session):
    template = FooTemplate(
        formula="price+price*inflation_rate*0.01",
        _question="Инфляция в год {inflation_rate}%. Сколько будет стоить хлеб через год, если сейчас он стоит {price}?",
        inflation_rate=(5,25), price=(100,1000)
    )
    sqla_task = template.generate_task()

    session.add(sqla_task)
    await session.commit()
    assert sqla_task.id is not None
    task = Task.from_db(sqla_task)
    assert task.template_name == sqla_task.template_name

