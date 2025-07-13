from typing import List, Optional

import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel


class TheoryFileLink(SQLModel, table=True):
    theory_id: Optional[int] = Field(
        default=None, foreign_key="theory.id", primary_key=True
    )
    file_id: Optional[int] = Field(
        default=None, foreign_key="file.id", primary_key=True
    )


class TheoryGraphLink(SQLModel, table=True):
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

    files: List["File"] = Relationship(
        back_populates="theories",
        link_model=TheoryFileLink,
    )

    graphs_datas: List["GraphData"] = Relationship(
        back_populates="theories",
        link_model=TheoryGraphLink,
    )
