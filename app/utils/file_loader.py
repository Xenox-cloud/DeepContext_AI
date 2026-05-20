"""
File Loader Utilities

Provides utilities for loading various file types.
"""

import os
import fitz
from docx import Document
from typing import Optional
from pathlib import Path
from app.core.logging import get_logger

logger = get_logger()

def load_pdf(path: str) -> str:

    doc = fitz.open(path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text

def load_docx(path: str) -> str:

    doc = Document(path)

    return "\n".join(
        para.text
        for para in doc.paragraphs
    )

def save_uploaded_file(file_content: bytes, filename: str, upload_dir: str) -> str:
    """
    Save uploaded file to disk.

    Args:
        file_content: File content as bytes
        filename: Original filename
        upload_dir: Directory to save file

    Returns:
        Path to saved file
    """
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, 'wb') as f:
        f.write(file_content)
    logger.info(f"Saved file: {file_path}")
    return file_path


def load_text_file(file_path: str) -> Optional[str]:
    """Load text from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading text file {file_path}: {e}")
        return None


def get_file_extension(filename: str) -> str:
    """Get file extension."""
    return Path(filename).suffix.lower().lstrip('.')
