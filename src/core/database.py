# src/core/database.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.models.product import Base as ProductBase
from src.models.event import Base as EventBase

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# -------- INITIALIZE TABLES -------- #
async def init_db():
    print("🔄 Connecting to database...")
    async with engine.begin() as conn:
        print("📌 Creating product tables...")
        await conn.run_sync(ProductBase.metadata.create_all)

        print("📌 Creating event tables...")
        await conn.run_sync(EventBase.metadata.create_all)

    print("✅ Database tables created!")


# Run directly: python -m src.core.database
if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
