from typing import List
from datetime import datetime


class Task:
    def __init__(self, task_id: str, skills_required: List[str], duration: int, deadline: datetime, priority: int):
        self.task_id = task_id
        self.skills_required = skills_required
        self.duration = duration
        self.deadline = deadline
        self.priority = priority
        self.assigned_worker = None
