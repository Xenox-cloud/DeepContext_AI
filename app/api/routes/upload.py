"""
Upload Route

Handles document upload endpoints.
"""

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.services.document_service import (
    DocumentService,
)


router = APIRouter()


ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt",
}


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload and register document.
    """

    file_extension = (
        file.filename.split(".")[-1].lower()
    )

    if file_extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type"
            ),
        )

    file_content = await file.read()

    document_service = DocumentService(db)

    document = (
        await document_service.create_document(
            file_content=file_content,
            original_filename=file.filename,
        )
    )
    await document_service.process_document(
        document
    )

    return {
        "id": document.id,
        "filename": document.filename,
        "original_filename": (
            document.original_filename
        ),
        "status": (
            document.processing_status
        ),
    }