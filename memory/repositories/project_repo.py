from memory.repositories.base import BaseRepository
from memory.models import Project
from shared.schemas.project_schemas import ProjectCreate, ProjectUpdate

class ProjectRepository(BaseRepository[Project, ProjectCreate, ProjectUpdate]):
    def __init__(self, db_session):
        super().__init__(Project)
        self.db = db_session
