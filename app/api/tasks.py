from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User
from schemas.schemas import TaskCreate, TaskUpdate
from core.deps import get_current_user, get_db
from services.task_service import TaskService

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def task_list(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    tasks = await TaskService.get_user_tasks(current_user, db)
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})

@router.post("/create")
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    task = await TaskService.create_task(current_user, task_data, db)
    return {"message": "Task added successfully", "task": task}

@router.put("/edit/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_task = await TaskService.update_task(task_id, task_data, db)
    return {"message": "Task updated", "task": updated_task}

@router.delete("/delete/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await TaskService.delete_task(task_id, db)
