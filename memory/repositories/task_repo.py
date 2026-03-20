from memory.repositories.base import BaseRepository
from memory.models import Task
from shared.schemas.task_schemas import TaskCreate, TaskUpdate

class TaskRepository(BaseRepository[Task, TaskCreate, TaskUpdate]):
    def __init__(self, db_session):
        super().__init__(Task)
        self.db = db_session
