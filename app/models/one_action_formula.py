from typing import Dict, Optional, List

import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel


class OneActionTaskLink(SQLModel, table=True):
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    oneactionformula_id: Optional[int] = Field(
        default=None, foreign_key="oneactionformula.id", primary_key=True
    )


class OneActionFormula(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    formula: Optional[str] = Field(default=None, max_length=255, sa_type=sa.String)
    question: str = Field(sa_type=sa.Text)
    param_ranges: Dict[str, list[int]] = Field(sa_type=sa.JSON)

    tasks: List["Task"] = Relationship(
        back_populates="one_action_formula",
        link_model=OneActionTaskLink,
    )
