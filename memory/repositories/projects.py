from memory.repositories.base import BaseRepository
from memory.models import Project, Task
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None

class ProjectUpdate(BaseModel):
    status: str

class ProjectRepository(BaseRepository[Project, ProjectCreate, ProjectUpdate]):
    pass

project_repo = ProjectRepository(Project)

class TaskCreate(BaseModel):
    project_id: str
    description: str
    assigned_agent_type: str

class TaskUpdate(BaseModel):
    status: str
    result_payload: dict | None = None

class TaskRepository(BaseRepository[Task, TaskCreate, TaskUpdate]):
    pass

task_repo = TaskRepository(Task)
