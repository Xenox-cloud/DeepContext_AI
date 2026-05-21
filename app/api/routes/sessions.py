"""
Session Routes
"""

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

from app.schemas.session_schema import (
    SessionResponse
)

from app.services.session_service import (
    SessionService
)

router = APIRouter()


@router.post(
    "/sessions/create",
    response_model=SessionResponse,
)
async def create_session(
    title: str = "New Chat",
    db: AsyncSession = Depends(
        get_db
    ),
):
    """
    Create chat session.
    """

    service = (
        SessionService(
            db
        )
    )

    session = await (
        service.create_session(
            title=title
        )
    )

    return {
        "session_id": (
            session.session_id
        ),
        "title": (
            session.title
        ),
    }