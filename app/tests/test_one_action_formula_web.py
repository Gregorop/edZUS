import pytest
from app.tests.boiler_for_one_formula import generate_given_to_bd
from app.models.one_action_formula import OneActionFormula
from sqlmodel import select


@pytest.mark.asyncio
async def test_create_formula(async_client, session):
    response = await async_client.post(
        "/one_action_formula/",
        json={
            "formula": "m*10*h",
            "question": (
                "Тело массой {m} кг, брошенное вертикально вверх, достигло максимальной высоты {h} м."
                "Какой кинетической энергией обладало тело сразу после броска? Сопротивлением воздуха пренебречь."
            ),
            "param_ranges": {"m": [1, 100], "h": [1, 100]},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["formula"] == "m*10*h"

    result = await session.execute(select(OneActionFormula))
    assert len(result.scalars().all()) == 1


@pytest.mark.asyncio
async def test_read_formulas(async_client, session):
    await generate_given_to_bd(session)

    response = await async_client.get("/one_action_formula/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["formula"] == "m*10*h"


@pytest.mark.asyncio
async def test_update_formula(async_client, session):
    create_response = await async_client.post(
        "/one_action_formula/",
        json={
            "formula": "m*10*h",
            "question": "Тело массой {m} кг с высоты {h}....",
            "param_ranges": {"m": [1, 100], "h": [1, 100]},
        },
    )
    assert create_response.status_code == 200
    created_data = create_response.json()
    formula_id = created_data["id"]

    update_response = await async_client.patch(
        f"/one_action_formula/{formula_id}",
        json={
            "formula": "m*9.8*h",
        },
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()

    assert updated_data["formula"] == "m*9.8*h"
    assert updated_data["param_ranges"] == {"m": [1, 100], "h": [1, 100]}

    result = await session.execute(
        select(OneActionFormula).where(OneActionFormula.id == formula_id)
    )

    db_formula = result.scalars().first()
    assert db_formula.formula == "m*9.8*h"
