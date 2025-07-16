import pytest
from app.models.theory import Theory
from sqlmodel import select


@pytest.mark.asyncio
async def test_create_theory(async_client, session):
    response = await async_client.post(
        "/theory/",
        json={
            "paragraphs": ["First paragraph", "Second paragraph"],
            "discipline": "Physics",
            "field": "Mechanics",
            "subfield": "Kinematics",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["discipline"] == "Physics"
    assert len(data["paragraphs"]) == 2

    result = await session.execute(select(Theory))
    assert len(result.scalars().all()) == 1


@pytest.mark.asyncio
async def test_read_theories(async_client, session):
    theories = [
        Theory(
            paragraphs=["Para 1", "Para 2"],
            discipline="Physics",
            field="Mechanics",
            subfield="Kinematics",
        ),
        Theory(
            paragraphs=["Intro"], discipline="Math", field="Algebra", subfield="Linear"
        ),
    ]
    session.add_all(theories)
    await session.commit()

    response = await async_client.get("/theory/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["discipline"] == "Physics"
    assert data[1]["discipline"] == "Math"


@pytest.mark.asyncio
async def test_update_theory(async_client, session):
    create_response = await async_client.post(
        "/theory/",
        json={
            "paragraphs": ["Old content"],
            "discipline": "Physics",
            "field": "Mechanics",
            "subfield": "Dynamics",
        },
    )
    assert create_response.status_code == 200
    created_data = create_response.json()
    theory_id = created_data["id"]

    update_response = await async_client.patch(
        f"/theory/{theory_id}",
        json={"paragraphs": ["Updated content"], "subfield": "Kinematics"},
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()

    assert updated_data["paragraphs"] == ["Updated content"]
    assert updated_data["subfield"] == "Kinematics"
    assert updated_data["discipline"] == "Physics"

    result = await session.execute(select(Theory).where(Theory.id == theory_id))
    db_theory = result.scalars().first()
    assert db_theory.paragraphs == ["Updated content"]


@pytest.mark.asyncio
async def test_delete_theory(async_client, session):
    create_response = await async_client.post(
        "/theory/",
        json={
            "paragraphs": ["To be deleted"],
            "discipline": "Test",
            "field": "Test",
            "subfield": "Test",
        },
    )
    assert create_response.status_code == 200
    created_data = create_response.json()
    theory_id = created_data["id"]

    result = await session.execute(select(Theory))
    assert len(result.scalars().all()) == 1

    delete_response = await async_client.delete(f"/theory/{theory_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"ok": True}

    result = await session.execute(select(Theory))
    assert len(result.scalars().all()) == 0
