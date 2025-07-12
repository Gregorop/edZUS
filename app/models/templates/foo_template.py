from random import randint
from ..base import DBTask
from ..task_template import BaseTaskTemplate

class FooTemplate(BaseTaskTemplate):
    def __init__(self, formula:str,_question, **_param_ranges):
        self._name = "тест уравнение"
        self._description = "Решение линейных уравнений вида ax + b = 0" 
        self._question_raw = _question

        self._formula = formula #для расчета ответа

        self._param_ranges = _param_ranges
    
    def _generate_params(self):
        self.params = {}
        for k, v in self._param_ranges.items():
            self.params[k] = randint(*v)

    def question(self) -> str:
        self._question = self._question_raw.format(**self.params)
        self._question += '\n Дано:'
        for k, v in self.params.items():
            self._question += f'{k} = {v} '
        self._question += "Успехов!"
        return self._question

    def generate_task(self) -> DBTask:
        self._generate_params() #каждый вызов - параметры обновляем
        safe_globals = {'__builtins__': None}
        result = eval(self._formula, safe_globals, self.params)
        
        return DBTask(
            template_name=self.name,
            question=self.question(),
            correct_answers=[result],
            variables=self.params
        )
