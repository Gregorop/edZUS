import pytest
from app.models.templates import OneActionFormulaTemplate
from app.models.one_action_tasks_templates import OneActionFormula
from sqlalchemy import select


@pytest.mark.asyncio
async def test_create_given_data(session):
    """пробнем сгенерить дано и задачи генератором по дано из бд"""

    given1 = OneActionFormula(
        formula="m*10*h",
        question=(
            "Тело массой {m} кг, брошенное вертикально вверх, достигло максимальной высоты {h} м."
            "Какой кинетической энергией обладало тело сразу после броска? Сопротивлением воздуха пренебречь."
        ),
        param_ranges={"m": (1, 100), "h": (1, 100)},
    )
    given2 = OneActionFormula(
        formula="Fa/10",
        question=(
            "На лодку, плавающую в воде, действует сила Архимеда величиной {Fa} Н. Чему равна масса лодки?"
        ),
        param_ranges={"Fa": (100, 1000)},
    )
    given3 = OneActionFormula(
        formula="u * 340",
        question=(
            "Человек услышал звук грома через {u} с после вспышки молнии."
            "Считая, что скорость звука в воздухе равна 340 м/с, определите, на каком расстоянии от человека ударила молния."
        ),
        param_ranges={"u": (1, 20)},
    )

    session.add_all([given1, given2, given3])
    await session.commit()

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
