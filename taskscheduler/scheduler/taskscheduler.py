from ..models.task import Task
from ..models.worker import Worker
from ..solvers.integer_solver import IntegerProgrammingSolver

class TaskScheduler:
    def __init__(self, solver):
        self.solver = solver

    def schedule(self, tasks: list[Task], workers: list[Worker]):
        return self.solver.solve(tasks, workers)
    

