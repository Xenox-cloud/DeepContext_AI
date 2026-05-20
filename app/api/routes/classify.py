"""
Classification Route

Provides document classification capabilities.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db
from typing import List

router = APIRouter()


@router.post("/classify")
async def classify_document(
    text: str,
    categories: List[str] = [],
    db: AsyncSession = Depends(get_db),
):
    """Classify a document into predefined categories."""
    return {
        "message": "Classification endpoint - implement classification service",
        "text": text[:100],
    }


@router.post("/classify/batch")
async def classify_batch(
    texts: List[str],
    db: AsyncSession = Depends(get_db),
):
    """Classify multiple documents."""
    return {"message": "Batch classification endpoint - implement"}
