"""
Database Session Module

Provides SQLAlchemy async session management
for PostgreSQL.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


# Create async SQLAlchemy engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)


# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database sessions.
    """

    async with AsyncSessionLocal() as session:
        try:
            yield session

        finally:
            await session.close()