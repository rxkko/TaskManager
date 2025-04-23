from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from schemas.schemas import LoginData, UserCreate
from core.security import create_access_token, authenticate_user
from crud.user import create_user

class AuthService:
    @staticmethod
    async def login(login_data: LoginData, db: AsyncSession):
        user = await authenticate_user(login_data.username, login_data.password, db)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = create_access_token({"sub": str(user.id)})

        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=3600,
            samesite="lax",
            secure=False
        )
        return response

    @staticmethod
    async def register(user_data: UserCreate, db: AsyncSession):
        try:
            user = await create_user(user_data, db)
            access_token = create_access_token(data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Пользователь уже существует")
