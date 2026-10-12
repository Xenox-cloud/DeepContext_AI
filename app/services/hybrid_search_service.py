"""
Hybrid Search Service
"""

import re

from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchAny,
)

from app.services.embedding_service import (
    EmbeddingService
)

from app.services.qdrant_service import (
    QdrantService
)


VECTOR_WEIGHT = 0.7
KEYWORD_WEIGHT = 0.3


def tokenize(
    text: str,
):

    return re.findall(
        r"\w+",
        text.lower(),
    )


class HybridSearchService:

    def __init__(self):

        self.embedding_service = (
            EmbeddingService()
        )

        self.qdrant_service = (
            QdrantService()
        )

    @staticmethod
    def keyword_score(
        query: str,
        text: str,
    ):
        """
        Fraction of distinct query terms that appear in the text (0.0 - 1.0).

        Kept on the same 0-1 scale as cosine similarity so neither signal
        swamps the other when they are combined.
        """

        query_terms = set(
            tokenize(query)
        )

        if not query_terms:

            return 0.0

        text_terms = set(
            tokenize(text)
        )

        return (
            len(query_terms & text_terms)
            /
            len(query_terms)
        )

    async def search(
        self,
        query: str,
        limit: int = 10,
        document_ids: list | None = None,
    ):

        embedding = (
            self.embedding_service.encode(
                [query]
            )[0]
        )

        # Restrict to the session's documents inside Qdrant, so the
        # candidate pool is never used up by other documents' chunks
        query_filter = None

        if document_ids:

            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchAny(
                            any=list(document_ids)
                        ),
                    )
                ]
            )

        results = await (
            self.qdrant_service.client.query_points(
                collection_name=(
                    self.qdrant_service.collection_name
                ),
                query=(
                    embedding.tolist()
                ),
                query_filter=query_filter,
                limit=limit * 3,
                with_payload=True,
            )
        )

        hybrid_results = []

        for point in results.points:

            payload = point.payload

            text = payload.get(
                "text",
                ""
            )

            vector_score = (
                point.score
            )

            keyword_score = (
                self.keyword_score(
                    query=query,
                    text=text,
                )
            )

            final_score = (
                (vector_score * VECTOR_WEIGHT)
                +
                (keyword_score * KEYWORD_WEIGHT)
            )

            hybrid_results.append(
                {
                    "text": text,
                    "score": final_score,
                    "vector_score": vector_score,
                    "keyword_score": keyword_score,
                    "payload": payload,
                }
            )

        hybrid_results = sorted(
            hybrid_results,
            key=lambda x: x["score"],
            reverse=True,
        )

        return hybrid_results[
            :limit
        ]
