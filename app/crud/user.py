from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.models import User
from schemas.schemas import UserCreate
from core.security import get_password_hash

async def create_user(user_data: UserCreate, db: AsyncSession):
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_username(username: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_email(email: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()
