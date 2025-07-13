from typing import Dict, Optional

import sqlalchemy as sa
from sqlmodel import Field

from app.models.base import BaseModel


class OneActionFormula(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    formula: Optional[str] = Field(default=None, max_length=255, sa_type=sa.String)
    question: str = Field(sa_type=sa.Text)
    param_ranges: Dict[str, list[int]] = Field(sa_type=sa.JSON)
