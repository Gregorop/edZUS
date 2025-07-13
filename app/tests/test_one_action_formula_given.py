import pytest
from sqlalchemy import select

from app.models.one_action_formula import OneActionFormula
from app.models.templates import OneActionFormulaTemplate
from app.tests.boiler_for_one_formula import generate_given_to_bd


@pytest.mark.asyncio
async def test_create_given_data(session):
    """пробнем сгенерить дано и задачи генератором по дано из бд"""

    await generate_given_to_bd(session)

    given_from_bd = await session.execute(select(OneActionFormula))

    for given in given_from_bd.scalars():
        template = OneActionFormulaTemplate(
            formula=given.formula,
            _question=given.question,
            **given.param_ranges,
        )

        task = template.generate_task()
        session.add(task)
        await session.commit()
        assert task.id is not None
        # print("Задача:")
        # print(task.question, task.correct_answers)
