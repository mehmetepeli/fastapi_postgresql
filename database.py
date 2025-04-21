from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Use asyncpg driver (note the +asyncpg in the URL)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:123456@localhost:5432/test_db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True  # Shows SQL queries in console
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()