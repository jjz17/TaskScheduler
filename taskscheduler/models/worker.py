from typing import List, Dict
from datetime import datetime


class Worker:
    def __init__(self, worker_id: str, skills: List[str], availability: Dict[datetime, bool], capacity: int):
        self.worker_id = worker_id
        self.skills = skills
        self.availability = availability
        self.capacity = capacity
