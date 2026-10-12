"""
Embedding Service
"""

from functools import lru_cache

from sentence_transformers import (
    SentenceTransformer
)


MODEL_NAME = "BAAI/bge-large-en-v1.5"


@lru_cache(maxsize=1)
def get_model():

    # Loaded once, on first use (the app preloads it at startup)
    return SentenceTransformer(
        MODEL_NAME
    )


class EmbeddingService:

    def __init__(self):

        self.model = get_model()

    def encode(
        self,
        texts,
    ):

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings
