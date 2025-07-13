from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_session
from app.models.one_action_formula import OneActionFormula

router = APIRouter(prefix="/one_action_formula")


@router.post("/", response_model=OneActionFormula)
async def create_formula(
    formula: OneActionFormula,
    session: AsyncSession = Depends(get_session),
):
    session.add(formula)
    await session.commit()
    await session.refresh(formula)
    return formula


@router.get("/", response_model=list[OneActionFormula])
async def read_formulas(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(OneActionFormula))
    return result.scalars().all()


@router.patch("/{formula_id}", response_model=OneActionFormula)
async def update_formula(
    formula_id: int,
    formula: OneActionFormula,
    session: AsyncSession = Depends(get_session),
):
    db_formula = await session.get(OneActionFormula, formula_id)
    if not db_formula:
        raise HTTPException(status_code=404, detail="Formula not found")

    for key, value in formula.model_dump(exclude_unset=True).items():
        setattr(db_formula, key, value)

    await session.commit()
    await session.refresh(db_formula)
    return db_formula


@router.delete("/{formula_id}")
async def delete_formula(formula_id: int, session: AsyncSession = Depends(get_session)):
    formula = await session.get(OneActionFormula, formula_id)
    if not formula:
        raise HTTPException(status_code=404, detail="Нет таких дано для задач!")
    await session.delete(formula)
    await session.commit()
    return {"ok": True}
