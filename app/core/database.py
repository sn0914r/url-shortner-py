from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text

from app.core.configs import configs

DATABASE_URL = configs.get("database_url")
if DATABASE_URL is None:
    raise ValueError("database_url is not set in configurations")

engine = create_async_engine(DATABASE_URL, echo=True)

session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def check_db_connection():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connected successfully")
    except Exception as e:
        print("Database connection failed")