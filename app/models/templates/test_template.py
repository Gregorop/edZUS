from random import randint
from ..task import Task
from ..task_template import ITaskTemplate

class TestTemplate(ITaskTemplate):
    def __init__(self):
        self._name = "тест уравнение"
        self._description = "Решение линейных уравнений вида ax + b = 0"
        #это для каждого типа задач будет захардкожено и норм
        self._param_ranges = {
            'a': (1, 10),
            'b': (1, 10)
        }
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    def generate_task(self) -> Task:
        a = randint(*self._param_ranges['a'])
        b = randint(*self._param_ranges['b'])
        
        f"Решите уравнение: {a}x + {b} = 0"
        correct_answer = -b / a
        
        return Task(
            template_name=self.name,
            correct_answer=correct_answer
            #и остальные нужные вещи
        )
