from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from models.models import Task, User
from schemas.schemas import TaskCreate, TaskUpdate

class TaskService:
    @staticmethod
    async def get_user_tasks(user: User, db: AsyncSession):
        result = await db.execute(select(Task).where(Task.user_id == user.id))
        return result.scalars().all()

    @staticmethod
    async def create_task(user: User, task_data: TaskCreate, db: AsyncSession):
        task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=user.id
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def update_task(task_id: int, task_data: TaskUpdate, db: AsyncSession):
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task.title = task_data.title
        task.description = task_data.description
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete_task(task_id: int, db: AsyncSession):
        task = await db.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        await db.delete(task)
        await db.commit()
        return {"message": "Task deleted successfully"}
