from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Union
from datetime import datetime
from app.models.task import Task
from app.models.one_action_formula import OneActionFormula
from app.core.database import get_session
from app.models.templates.one_action_formula_template import OneActionFormulaTemplate

router = APIRouter(prefix="/tasks")


@router.post("/generate_from_formula/{formula_id}", response_model=Task)
async def generate_task_from_formula(
    formula_id: int,
    session: AsyncSession = Depends(get_session),
):
    formula = await session.get(OneActionFormula, formula_id)
    if not formula:
        raise HTTPException(status_code=404, detail="Formula not found")

    generator = OneActionFormulaTemplate(
        formula=formula.formula,
        _question=formula.question,
        **formula.param_ranges,
    )

    task = generator.generate_task()

    task.one_action_formulas = [formula]

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


@router.get("/", response_model=List[Task])
async def read_tasks(session: AsyncSession = Depends(get_session)):
    return await session.execute(select(Task)).all()


@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task_update: Task,
    session: AsyncSession = Depends(get_session),
):
    db_task = await session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    await session.commit()
    await session.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
async def delete_task(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(task)
    await session.commit()
    return {"ok": True}


@router.post("/check_answer/{task_id}", response_model=dict)
async def check_task_answer(
    task_id: int,
    user_answer: List[Union[str, int, float]],
    session: AsyncSession = Depends(get_session),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    is_correct = sorted(user_answer) == sorted(task.correct_answers)

    task.user_answers = user_answer
    task.solved_at = datetime.now()

    await session.commit()
    await session.refresh(task)

    return {
        "is_correct": is_correct,
        "correct_answers": task.correct_answers,
        "task": task,
    }
