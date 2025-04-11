from pydantic import BaseModel, EmailStr
import datetime


class UserCreate(BaseModel):
    id: int
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

    class Config:
        orm_mode = True


# class TaskWithUser(TaskCreate):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True