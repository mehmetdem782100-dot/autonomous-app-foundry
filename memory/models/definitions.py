import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, Enum, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from memory.database import Base

class ProjectStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TaskStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    NEEDS_REWORK = "NEEDS_REWORK"
    FAILED = "FAILED"

class LogLevel(str, enum.Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    parent_task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True)
    description = Column(Text, nullable=False)
    assigned_agent_type = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.QUEUED)
    result_payload = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    version_id = Column(Integer, nullable=False, default=1)
    
    __mapper_args__ = {
        "version_id_col": version_id
    }
    
    project = relationship("Project", back_populates="tasks")

class AgentLog(Base):
    __tablename__ = "agent_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    agent_type = Column(String, nullable=False)
    log_level = Column(Enum(LogLevel), default=LogLevel.INFO)
    message = Column(Text, nullable=False)
    llm_prompt = Column(Text, nullable=True)
    llm_response = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SystemSnapshot(Base):
    __tablename__ = "system_snapshots"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    file_tree_state = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
