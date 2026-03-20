from pydantic import BaseModel, Field, UUID4
from typing import Dict, Any, Optional
from datetime import datetime

class TaskEventPayload(BaseModel):
    task_id: UUID4
    project_id: UUID4
    agent_type: str
    action: str
    context: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class TaskResultPayload(BaseModel):
    task_id: UUID4
    status: str
    output: Dict[str, Any]
    error_message: Optional[str] = None
