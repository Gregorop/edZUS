from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List, Union, Literal
from datetime import datetime
from app.models.base import DBTask, DBGraphData, DBTaskImage

class TaskImage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    base64: str
    mime_type: str  # "image/png", "image/jpeg"

class GraphData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: Literal["line", "histogram"]
    x: List[Union[float, str]]
    y: List[float]
    options: Dict[str, Any] = {}

class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    template_name: str
    question: str
    answer_options: list[str] = []
    correct_answers: list[str]
    user_answers: list[str] = None
    is_solved: bool = False

    graph: Optional[GraphData] = None
    image: Optional[TaskImage] = None

    table: dict[str, Any] = {}
    variables: dict[str, Any] = {}
    formula: Optional[str] = None

    created_at: datetime = datetime.now()
    solved_at: datetime

    @classmethod
    def from_db(cls, db_obj) -> 'Task':
        return cls.model_validate(db_obj)

    def to_orm(self) -> DBTask:
        db_task = DBTask(**self.model_dump(exclude={"graph", "image"}))
        
        if self.graph:
            db_task.graph = DBGraphData(**self.graph.model_dump())
        
        if self.image:
            db_task.image = DBTaskImage(**self.image.model_dump())
            
        return db_task
