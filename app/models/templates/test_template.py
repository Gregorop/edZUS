from random import randint
from ..base import DBTask
from ..task_template import BaseTaskTemplate

class TestTemplate(BaseTaskTemplate):
    def __init__(self, formula:str, **_param_ranges):
        self._name = "тест уравнение"
        self._description = "Решение линейных уравнений вида ax + b = 0"
        #это для каждого типа задач будет захардкожено и норм
        self._formula = formula # TODO нужно еще to_show_formula, что будет показываться ученику. А эта для расчета ответа
        #надо получать аргументами в генератор
        self._param_ranges = _param_ranges
        self._generate_params()
    
    def _generate_params(self):
        self.params = {}
        for k, v in self._param_ranges.items():
            self.params[k] = randint(*v)

    def question(self) -> str:
        quest = f'решите уравнение {self._formula}, если: '
        for k, v in self.params.items():
            quest += f'{k} = {v} '
        quest += "Успехов!"
        return quest

    def generate_task(self) -> DBTask:
        quest = self.question()
        safe_globals = {'__builtins__': None}
        result = eval(self._formula, safe_globals, self.params)
        
        return DBTask(
            template_name=self.name,
            question=quest,
            correct_answers=[result]
        )
