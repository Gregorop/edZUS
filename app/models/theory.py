from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship

from app.models.base import BaseModel
from app.models.task import TaskTheoryLink


class TheoryFileLink(BaseModel, table=True):
    theory_id: Optional[int] = Field(
        default=None, foreign_key="theory.id", primary_key=True
    )
    file_id: Optional[int] = Field(
        default=None, foreign_key="file.id", primary_key=True
    )


class TheoryGraphLink(BaseModel, table=True):
    theory_id: Optional[int] = Field(
        default=None, foreign_key="theory.id", primary_key=True
    )
    graph_id: Optional[int] = Field(
        default=None, foreign_key="graphdata.id", primary_key=True
    )


class Theory(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paragraphs: list[str] = Field(default=[], sa_type=sa.ARRAY(sa.String))
    discipline: str = Field(sa_type=sa.Text)
    field: str = Field(sa_type=sa.Text)
    subfield: str = Field(sa_type=sa.Text)

    tasks: Mapped[List["Task"]] = Relationship(
        back_populates="theories",
        link_model=TaskTheoryLink,
    )

    files: Mapped[List["File"]] = Relationship(
        back_populates="theories",
        link_model=TheoryFileLink,
    )

    graphs_datas: Mapped[List["GraphData"]] = Relationship(
        back_populates="theories",
        link_model=TheoryGraphLink,
    )
