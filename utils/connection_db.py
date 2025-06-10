from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel

DATABASE_URL = (
    "postgresql+asyncpg://ubydtzfq76agbyx9yxwr:XIiqD55NfbI6HMVOkWJWdUNSquwC4c@"
    "btng9poyhgttpjvdekzs-postgresql.services.clever-cloud.com:50013/"
    "btng9poyhgttpjvdekzs"
)

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=5,
    max_overflow=0,
    pool_timeout=30,
    pool_recycle=1800
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session