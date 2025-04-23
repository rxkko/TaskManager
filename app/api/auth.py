from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas import UserCreate, Token, LoginData
from database import get_db
from services.auth_service import AuthService

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/login")
async def login(
    login_data: LoginData,
    db: AsyncSession = Depends(get_db)
):
    return await AuthService.login(login_data, db)

@router.post("/register", response_model=Token)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await AuthService.register(user_data, db)

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
