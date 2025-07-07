from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, JSON, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base() 

class DBBaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))


class DBTaskImage(DBBaseModel):
    __tablename__ = "task_images"
    
    base64 = Column(Text, nullable=False)
    mime_type = Column(String(50), nullable=False)


class DBGraphData(DBBaseModel):
    __tablename__ = "graph_data"
    
    type = Column(String(20), nullable=False)
    x = Column(JSON, nullable=False)
    y = Column(JSON, nullable=False)
    options = Column(JSON, default={})


class DBTask(DBBaseModel):
    __tablename__ = "tasks"
    
    template_name = Column(String(100), nullable=False)
    question = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    is_solved = Column(Boolean, default=False)
    user_answer = Column(Text)

    graph_id = Column(Integer, ForeignKey("graph_data.id"))
    graph = relationship("GraphData", backref="tasks")
    
    image_id = Column(Integer, ForeignKey("task_images.id"))
    image = relationship("TaskImage", backref="tasks")
