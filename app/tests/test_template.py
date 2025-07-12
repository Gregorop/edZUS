import pytest
from app.models.templates import OneActionFormulaTemplate


@pytest.mark.asyncio
async def test_task_create(session):
    template = OneActionFormulaTemplate(
        formula="price+price*inflation_rate*0.01",
        _question="Инфляция в год {inflation_rate}%. Сколько будет стоить хлеб через год, если сейчас он стоит {price}?",
        inflation_rate=(5,25), price=(100,1000)
    )

    task = template.generate_task()
    session.add(task)
    await session.commit()
    assert task.id is not None
