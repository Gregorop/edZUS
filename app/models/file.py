from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship

from app.models.base import BaseModel

from .task import TaskFileLink
from .theory import TheoryFileLink


class File(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_path: str = Field(sa_type=sa.String(500))
    file_name: str = Field(max_length=255, sa_type=sa.String)
    file_extension: str = Field(max_length=20, sa_type=sa.String)

    tasks: Mapped[List["Task"]] = Relationship(
        back_populates="files", link_model=TaskFileLink
    )
    theories: Mapped[List["Theory"]] = Relationship(
        back_populates="files", link_model=TheoryFileLink
    )
