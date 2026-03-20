from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from typing import Optional, Any, Dict
from memory.models import TaskStatus

class TaskBase(BaseModel):
    description: str
    assigned_agent_type: str
    project_id: UUID4

class TaskCreate(TaskBase):
    parent_task_id: Optional[UUID4] = None

class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    result_payload: Optional[Dict[str, Any]] = None

class TaskInDB(TaskBase):
    id: UUID4
    status: TaskStatus
    result_payload: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
