from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from memory.database import get_db
from memory.repositories.project_repo import ProjectRepository
from memory.repositories.task_repo import TaskRepository

async def get_project_repo(db: AsyncSession = Depends(get_db)) -> ProjectRepository:
    return ProjectRepository(db)

async def get_task_repo(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)
