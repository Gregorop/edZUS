from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_session
from app.models.theory import Theory

router = APIRouter(prefix="/theory")


@router.post("/", response_model=Theory)
async def create_theory(
    theory: Theory,
    session: AsyncSession = Depends(get_session),
):
    session.add(theory)
    await session.commit()
    await session.refresh(theory)
    return theory


@router.get("/", response_model=list[Theory])
async def read_theories(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Theory))
    return result.scalars().all()


@router.patch("/{theory_id}", response_model=Theory)
async def update_theory(
    theory_id: int,
    theory: Theory,
    session: AsyncSession = Depends(get_session),
):
    db_theory = await session.get(Theory, theory_id)
    if not db_theory:
        raise HTTPException(status_code=404, detail="Theory not found")

    for key, value in theory.model_dump(exclude_unset=True).items():
        setattr(db_theory, key, value)

    await session.commit()
    await session.refresh(db_theory)
    return db_theory


@router.delete("/{theory_id}")
async def delete_theory(theory_id: int, session: AsyncSession = Depends(get_session)):
    theory = await session.get(Theory, theory_id)
    if not theory:
        raise HTTPException(status_code=404, detail="Theory not found")
    await session.delete(theory)
    await session.commit()
    return {"ok": True}
