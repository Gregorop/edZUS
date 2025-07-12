from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

Base = SQLModel

class BaseModel(SQLModel):
    """Базовая модель для Pydantic и SQLAlchemy"""
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime = Field(default_factory=datetime.now)
