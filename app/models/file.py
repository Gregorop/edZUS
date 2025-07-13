from typing import List, Optional

import sqlalchemy as sa
from sqlmodel import Field, Relationship

from app.models.base import BaseModel


class File(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_path: str = Field(sa_type=sa.String(500))
    file_name: str = Field(max_length=255, sa_type=sa.String)
    file_extension: str = Field(max_length=20, sa_type=sa.String)

    tasks: List["Task"] = Relationship(back_populates="file")
    theories: List["Theory"] = Relationship(back_populates="file")
