from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import sqlalchemy as sa
from sqlmodel import Field, Relationship

from app.models.base import BaseModel


class TaskFileLink(BaseModel, table=True):
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    file_id: Optional[int] = Field(
        default=None, foreign_key="file.id", primary_key=True
    )


class TaskGraphLink(BaseModel, table=True):
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    graph_id: Optional[int] = Field(
        default=None, foreign_key="graphdata.id", primary_key=True
    )


class TaskTheoryLink(BaseModel, table=True):
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    theory_id: Optional[int] = Field(
        default=None, foreign_key="theory.id", primary_key=True
    )


class Task(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    template_name: str = Field(max_length=100, sa_type=sa.String)

    question: str = Field(sa_type=sa.Text)
    answer_options: List[Union[str, int, float]] = Field(default=[], sa_type=sa.JSON)
    correct_answers: List[Union[str, int, float]] = Field(sa_type=sa.JSON)
    user_answers: Optional[List[Union[str, int]]] = Field(default=None, sa_type=sa.JSON)
    solved_at: Optional[datetime] = None

    table: Dict[str, Any] = Field(default={}, sa_type=sa.JSON)
    variables: Dict[str, Any] = Field(default={}, sa_type=sa.JSON)
    formula: Optional[str] = Field(default=None, max_length=255, sa_type=sa.String)

    files: List["File"] = Relationship(
        back_populates="tasks",
        link_model=TaskFileLink,
    )

    graphs_datas: List["GraphData"] = Relationship(
        back_populates="tasks",
        link_model=TaskGraphLink,
    )

    theories: List["Theory"] = Relationship(
        back_populates="tasks",
        link_model=TaskTheoryLink,
    )
