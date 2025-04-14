from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool = False

    class Config:
        orm_mode = True

        
class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    username: str
    password: str

class LoginData(BaseModel):
    username: str
    password: str