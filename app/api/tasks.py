from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
    title: str = Form(...),
    description: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    await db.commit()
    return RedirectResponse(url="/tasks", status_code=303)


@router.post("/edit/{task_id}")
async def update_task(
    task_id: int,
    new_title: str = Form(...),
    new_description: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    task = await db.execute(select(Task).filter(Task.id == task_id))

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = new_title
    task.description = new_description
    db.add(task)
    await db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.post("/delete/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(Task, task_id)
    if task:
        await db.delete(task)
        await db.commit()
    return RedirectResponse(url="/tasks", status_code=303)