from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings
from sqlalchemy.exc import SQLAlchemyError
from models.models import Base


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    future=True,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
    

async def create_tables():
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as e:
        print(f"Ошибка при создании таблиц: {e}")

async def get_db():
    async with async_session() as session:
        yield session

