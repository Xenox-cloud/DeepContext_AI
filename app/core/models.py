"""
Global AI Models
"""

from sentence_transformers import (
    SentenceTransformer,
)

embedding_model = (
    SentenceTransformer(
        "BAAI/bge-large-en-v1.5"
    )
)