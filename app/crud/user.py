from sqlalchemy.ext.asyncio import AsyncSession
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