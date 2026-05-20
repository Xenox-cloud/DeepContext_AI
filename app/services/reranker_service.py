"""
Reranker Service
"""

from sentence_transformers import (
    CrossEncoder
)


RERANK_MODEL = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


class RerankerService:

    def __init__(self):

        self.model = (
            RERANK_MODEL
        )

    def rerank(
        self,
        query: str,
        documents: list[str],
        top_k: int = 5,
    ):

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