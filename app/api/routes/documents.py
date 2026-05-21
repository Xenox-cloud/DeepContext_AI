"""
Documents Route
"""

import os

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

from app.db.models.chunk import (
    Chunk
)

from app.db.models.document import (
    Document
)

from app.schemas.document_schema import (
    DocumentResponse
)

router = APIRouter()


@router.get(
    "/documents",
)
async def list_documents(
    db: AsyncSession = Depends(
        get_db
    ),
):
    """
    List uploaded documents.
    """

    stmt = select(
        Document
    )

    result = await db.execute(
        stmt
    )

    documents = (
        result.scalars().all()
    )

    return [
        {
            "id": document.id,
            "filename": (
                document.original_filename
            ),
            "original_filename": (
                document.original_filename
            ),
            "status": (
                document.processing_status
            ),
        }
        for document in documents
    ]


@router.get(
    "/documents/{document_id}",
    response_model=DocumentResponse,
)
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(
        get_db
    ),
):
    """
    Get single document.
    """

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

    return {
        "id": document.id,
        "filename": (
            document.filename
        ),
        "original_filename": (
            document.original_filename
        ),
        "status": (
            document.processing_status
        ),
    }


@router.get(
    "/documents/{document_id}/chunks",
)
async def get_document_chunks(
    document_id: int,
    db: AsyncSession = Depends(
        get_db
    ),
):
    """
    Get document chunks.
    """

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

    chunk_stmt = select(
        Chunk
    ).where(
        Chunk.document_id
        ==
        document_id
    )

    chunk_result = await db.execute(
        chunk_stmt
    )

    chunks = (
        chunk_result.scalars().all()
    )

    return {
        "document": {
            "id": document.id,
            "filename": (
                document.original_filename
            ),
        },
        "chunks": [
            {
                "id": chunk.id,
                "chunk_index": (
                    chunk.chunk_index
                ),
                "text": (
                    chunk.text
                ),
                "qdrant_point_id": (
                    chunk.qdrant_point_id
                ),
            }
            for chunk in chunks
        ],
    }


@router.delete(
    "/documents/{document_id}",
)
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(
        get_db
    ),
):
    """
    Delete document.
    """

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

    if os.path.exists(
        document.file_path
    ):

        os.remove(
            document.file_path
        )

    await db.delete(
        document
    )

    await db.commit()

    return {
        "message": (
            "Document deleted successfully"
        )
    }