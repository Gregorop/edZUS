from abc import ABC, abstractmethod
from app.models.task import Task

class ITaskTemplate(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Уникальное имя"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Описание шаблона"""
        pass
    
    
    @abstractmethod
    def generate_task(self) -> Task:
        """Генерирует конкретную задачу на основе шаблона"""
        pass
