"""
Health Check Route

Provides health check endpoint for monitoring and load balancing.
"""

from fastapi import APIRouter, Depends, status
from app.api.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint."""
    return {
        "status": "healthy",
    }
