from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import sqlalchemy as sa
from sqlmodel import Field, Relationship

from app.models.base import BaseModel


class GraphType(str, Enum):
    line = "line"
    histogram = "histogram"

class TaskImage(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    base64: str = Field(sa_type=sa.Text)
    mime_type: str = Field(max_length=50,sa_type=sa.String)  # "image/png", "image/jpeg"

    tasks: List["Task"] = Relationship(back_populates="image")

class GraphData(BaseModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: GraphType = Field(max_length=20)
    x: List[Union[float, str]] = Field(sa_type=sa.JSON)
    y: List[float] = Field(sa_type=sa.JSON)
    options: Dict[str, Any] = Field(default={}, sa_type=sa.JSON)

    tasks: List["Task"] = Relationship(back_populates="graph")

class Task(BaseModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    template_name: str = Field(max_length=100,sa_type=sa.String)

    question: str = Field(sa_type=sa.Text)
    answer_options: List[Union[str, int, float]] = Field(default=[], sa_type=sa.JSON)
    correct_answers: List[Union[str, int, float]] = Field(sa_type=sa.JSON)
    user_answers: Optional[List[Union[str, int]]] = Field(default=None, sa_type=sa.JSON)
    solved_at: Optional[datetime] = None

    table: Dict[str, Any] = Field(default={}, sa_type=sa.JSON)
    variables: Dict[str, Any] = Field(default={}, sa_type=sa.JSON)
    formula: Optional[str] = Field(default=None, max_length=255,sa_type=sa.String)

    graph_id: Optional[int] = Field(default=None, foreign_key="graphdata.id")
    graph: Optional[GraphData] = Relationship(back_populates="tasks")

    image_id: Optional[int] = Field(default=None, foreign_key="taskimage.id")
    image: Optional[TaskImage] = Relationship(back_populates="tasks")
