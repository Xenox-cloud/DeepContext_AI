"""
Reranker Service
"""

from functools import lru_cache

from sentence_transformers import (
    CrossEncoder
)


RERANK_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


@lru_cache(maxsize=1)
def get_rerank_model():

    # Loaded once, on first use
    return CrossEncoder(
        RERANK_MODEL_NAME
    )


class RerankerService:

    def __init__(self):

        self.model = (
            get_rerank_model()
        )

    def rerank(
        self,
        query: str,
        documents: list[str],
        top_k: int = 5,
    ):

        if not documents:

            return []

        pairs = [
            [query, doc]
            for doc in documents
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked[:top_k]
