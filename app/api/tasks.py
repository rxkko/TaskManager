from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.schemas import TaskCreate, TaskUpdate

from database import get_db
from models.models import Task


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def task_list(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})


@router.post("/create")
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    new_task = Task(**task.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)


@router.put("/edit/{task_id}")
async def update_task(
    task_id: int,
    update_task: TaskUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = update_task.title
    task.description = update_task.description
    await db.commit()
    await db.refresh(task)
    #return task


@router.delete("/delete/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(Task, task_id)
    if task:
        await db.delete(task)
        await db.commit()
