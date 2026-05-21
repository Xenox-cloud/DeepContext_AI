"""
Classification Route

Provides document classification capabilities.
"""

from typing import (
    List
)

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.api.dependencies import (
    get_db
)

router = APIRouter()


@router.post(
    "/classify",
)
async def classify_document(
    text: str,
    categories: List[str] | None = None,
    db: AsyncSession = Depends(
        get_db
    ),
):
    """
    Classify a document into
    predefined categories.
    """

    if categories is None:

        categories = []

    return {
        "message": (
            "Classification endpoint "
            "- implement classification service"
        ),
        "text": (
            text[:100]
        ),
        "categories": (
            categories
        ),
    }


@router.post(
    "/classify/batch",
)
async def classify_batch(
    texts: List[str],
    db: AsyncSession = Depends(
        get_db
    ),
):
    """
    Classify multiple documents.
    """

    return {
        "message": (
            "Batch classification endpoint "
            "- implement"
        ),
        "total_documents": (
            len(texts)
        ),
    }