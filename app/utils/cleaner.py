"""
Text Cleaning Utilities

Provides text cleaning and preprocessing utilities.
"""

import re
from app.core.logging import get_logger

logger = get_logger()


def clean_text(text: str) -> str:
    """
    Clean and preprocess text.

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    logger.debug(f"Cleaning text of length {len(text)}")

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove special characters (keep alphanumeric, punctuation, spaces)
    text = re.sub(r'[^\w\s.,!?;:()\-"\']', '', text)

    return text.strip()


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    return ' '.join(text.split())


def remove_html_tags(text: str) -> str:
    """Remove HTML tags from text."""
    return re.sub(r'<[^>]+>', '', text)
