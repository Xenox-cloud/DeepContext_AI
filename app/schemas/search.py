"""
Search Schemas

Pydantic schemas for search-related API operations.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class SearchRequest(BaseModel):
    """Schema for search request."""
    query: str = Field(..., description="Search query text")
    top_k: int = Field(10, ge=1, le=50, description="Number of results")
    score_threshold: Optional[float] = Field(None, description="Minimum score threshold")
    filters: Optional[dict] = Field(None, description="Optional filters")


class SearchResult(BaseModel):
    """Schema for search result."""
    id: int
    content: str
    score: float
    document_id: int
    document_filename: str
    chunk_index: int


class SearchResponse(BaseModel):
    """Schema for search response."""
    results: List[SearchResult]
    total: int
    query: str
