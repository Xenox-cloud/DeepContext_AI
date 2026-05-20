"""
Embedding Service
"""

from sentence_transformers import (
    SentenceTransformer
)


MODEL = SentenceTransformer(
    "BAAI/bge-large-en-v1.5"
)


class EmbeddingService:

    def __init__(self):

        self.model = MODEL

    def encode(
        self,
        texts,
    ):

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings