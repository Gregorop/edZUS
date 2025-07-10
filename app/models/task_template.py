from abc import ABC, abstractmethod
from app.models.task import Task

class ITaskTemplate(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Уникальное имя шаблона"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Описание шаблона"""
        pass
    
    @property
    @abstractmethod
    def question(self) -> str:
        """Текст вопроса задачи, может быть строкой, либо в нее надо подставлять переменные"""
        pass

    @abstractmethod
    def generate_task(self) -> Task:
        """Генерирует конкретную задачу на основе захардкоженной логики"""
        pass

class BaseTaskTemplate(ITaskTemplate):
    def __init__(self, name: str, description: str):
        self._name = name
        self._description = description
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
