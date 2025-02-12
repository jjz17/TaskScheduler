from fastapi import FastAPI
from ..scheduler.taskscheduler import TaskScheduler
from ..solvers.integer_solver import IntegerProgrammingSolver

app = FastAPI()
scheduler = TaskScheduler(IntegerProgrammingSolver())

@app.get("/assign_tasks")
def assign_tasks():
    tasks = get_tasks_from_db()
    workers = get_workers_from_db()
    assignments = scheduler.schedule(tasks, workers)
    return {"assignments": [assignment.__dict__ for assignment in assignments]}
