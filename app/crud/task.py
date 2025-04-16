from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.schemas import TaskCreate, TaskUpdate
from database import get_db
from models.models import Task, User
from core.deps import get_current_user
from fastapi.responses import HTMLResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def task_list(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.user_id == current_user.id))
    tasks = result.scalars().all()
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})

@router.post("/create")
async def create_task(task_data: TaskCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user.id
    )
    db.add(task)
    await db.commit()
    return {"message": "Task added successfully", "task": task}


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


@router.delete("/delete/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(Task, task_id)
    if task:
        await db.delete(task)
        await db.commit()
