"""
API Dependencies Module

Defines dependency injection functions for FastAPI routes.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.core.logging import get_logger

logger = get_logger()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session.
    """

    async with AsyncSessionLocal() as session:
        yield session