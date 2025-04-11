from fastapi import FastAPI
from database import create_tables
from contextlib import asynccontextmanager
from api import tasks
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])



@app.get("/")
async def root():
    return {"message": "Добро пожаловать в Task Manager!"}
