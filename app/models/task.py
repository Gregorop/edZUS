from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List, Union, Literal
from datetime import datetime
from base import DBTask, DBGraphData, DBTaskImage

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
    correct_answer: Any
    graph: Optional[GraphData] = None
    image: Optional[TaskImage] = None
    is_solved: bool = False
    user_answer: Optional[Any] = None
    created_at: datetime = datetime.now()

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
