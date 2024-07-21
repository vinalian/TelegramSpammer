from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from os import environ
from contextlib import asynccontextmanager

__all__ = ['database']

SQLALCHEMY_DATABASE_URI = (
    f'postgresql+asyncpg://'
    f'{environ.get("POSTGRES_USER")}:'
    f'{environ.get("POSTGRES_PASSWORD")}@'
    f'{environ.get("POSTGRES_HOST")}:'
    f'{environ.get("POSTGRES_PORT")}/'
    f'{environ.get("POSTGRES_DB")}'
)

# Create an asynchronous SQLAlchemy engine
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=False,
    pool_size=10,  # connection pool size
    max_overflow=20  # number of additional connections if the pool is exhausted
)

# Create a SQLAlchemy session factory
async_session_factory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Context manager for managing sessions
@asynccontextmanager
async def get_session():
    async with async_session_factory() as session:
        yield session


class DatabaseSession:
    @staticmethod
    async def create_session() -> AsyncSession:
        """
        Creates and returns an asynchronous session.
        :return: AsyncSession
        """
        async with get_session() as session:
            return session


# Create an instance of the class for working with the database.
database = DatabaseSession()
