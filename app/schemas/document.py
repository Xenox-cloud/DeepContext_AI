"""
Document Schemas

Pydantic schemas for document-related API operations.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DocumentCreate(BaseModel):
    """Schema for creating a document."""
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="File type (txt, pdf, docx, etc.)")
    file_size: int = Field(..., description="File size in bytes")
    metadata_json: Optional[str] = Field(None, description="JSON metadata")


class DocumentResponse(BaseModel):
    """Schema for document response."""
    id: int
    filename: str
    file_type: str
    file_size: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Schema for list of documents."""
    documents: List[DocumentResponse]
    total: int
