from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, List
from memory.models import ProjectStatus

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    status: Optional[ProjectStatus] = None
    name: Optional[str] = None

class ProjectInDB(ProjectBase):
    id: UUID4
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
