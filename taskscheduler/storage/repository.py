# Repository for Database Operations
class TaskRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def add_task(self, task: TaskDB):
        self.db.add(task)
        self.db.commit()
    
    def get_tasks(self):
        return self.db.query(TaskDB).all()

class WorkerRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def add_worker(self, worker: WorkerDB):
        self.db.add(worker)
        self.db.commit()
    
    def get_workers(self):
        return self.db.query(WorkerDB).all()

class AssignmentRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def add_assignment(self, assignment: AssignmentDB):
        self.db.add(assignment)
        self.db.commit()
    
    def get_assignments(self):
        return self.db.query(AssignmentDB).all()