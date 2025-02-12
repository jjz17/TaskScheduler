from typing import List, Dict
from datetime import datetime, timedelta

from task import Task
from worker import Worker


class Assignment:
    def __init__(self, task: Task, worker: Worker, start_time: datetime):
        self.task = task
        self.worker = worker
        self.start_time = start_time
        self.end_time = start_time + timedelta(minutes=task.duration)