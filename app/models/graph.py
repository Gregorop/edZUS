from enum import Enum
from typing import Any, Dict, List, Optional, Union

import sqlalchemy as sa
from sqlmodel import Field, Relationship

from app.models.base import BaseModel


class GraphType(str, Enum):
    line = "line"
    histogram = "histogram"


class GraphData(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: GraphType = Field(max_length=20)
    x: List[Union[float, str]] = Field(sa_type=sa.JSON)
    y: List[float] = Field(sa_type=sa.JSON)
    options: Dict[str, Any] = Field(default={}, sa_type=sa.JSON)

    tasks: List["Task"] = Relationship(back_populates="image")
    theories: List["Theory"] = Relationship(back_populates="image")
