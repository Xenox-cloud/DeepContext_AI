"""
Session Document Routes
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.api.dependencies import (
    get_db
)

from app.db.models.chat_session import (
    ChatSession
)

from app.db.models.document import (
    Document
)

from app.schemas.session_schema import (
    SessionResponse
)

from app.services.session_service import (
    SessionService
)

router = APIRouter()


@router.post(
    "/sessions/{session_id}/documents/{document_id}",
)
async def attach_document_to_session(
    session_id: str,
    document_id: int,
    db: AsyncSession = Depends(
        get_db
    ),
):
    """
    Attach document to session.
    """

    stmt = select(
        ChatSession
    ).where(
        ChatSession.session_id
        ==
        session_id
    )

    result = await db.execute(
        stmt
    )

    session = (
        result.scalar_one_or_none()
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    stmt = select(
        Document
    ).where(
        Document.id
        ==
        document_id
    )

    result = await db.execute(
        stmt
    )

    document = (
        result.scalar_one_or_none()
    )

    if not document:

        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    service = (
        SessionService(
            db
        )
    )

    await service.attach_document(
        session_db_id=(
            session.id
        ),
        document_id=(
            document.id
        ),
    )

    return {
        "message": (
            "Document attached successfully"
        ),
        "session_id": (
            session_id
        ),
        "document_id": (
            document_id
        ),
    }