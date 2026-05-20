"""
Classification Schemas

Pydantic schemas for classification-related API operations.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ClassificationRequest(BaseModel):
    """Schema for classification request."""
    text: str = Field(..., description="Text to classify")
    categories: Optional[List[str]] = Field(None, description="Predefined categories")


class ClassificationResult(BaseModel):
    """Schema for classification result."""
    category: str
    confidence: float
    label: str


class ClassificationResponse(BaseModel):
    """Schema for classification response."""
    text: str
    results: List[ClassificationResult]
