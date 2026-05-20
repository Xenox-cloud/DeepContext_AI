"""
Hybrid Search Service
"""

from collections import Counter

from app.services.embedding_service import (
    EmbeddingService
)

from app.services.qdrant_service import (
    QdrantService
)


class HybridSearchService:

    def __init__(self):

        self.embedding_service = (
            EmbeddingService()
        )

        self.qdrant_service = (
            QdrantService()
        )

    def keyword_score(
        self,
        query: str,
        text: str,
    ):

        query_words = (
            query.lower().split()
        )

        text_words = (
            text.lower().split()
        )

        text_counter = Counter(
            text_words
        )

        score = 0

        for word in query_words:

            score += (
                text_counter[word]
            )

        return score

    async def search(
        self,
        query: str,
        limit: int = 10,
    ):

        embedding = (
            self.embedding_service.encode(
                [query]
            )[0]
        )

        results = await (
            self.qdrant_service.client.query_points(
                collection_name=(
                    self.qdrant_service.collection_name
                ),
                query=(
                    embedding.tolist()
                ),
                limit=limit * 3,
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
                (vector_score * 0.7)
                +
                (keyword_score * 0.3)
            )

            hybrid_results.append(
                {
                    "text": text,
                    "score": final_score,
                    "payload": payload,
                }
            )

        hybrid_results = sorted(
            hybrid_results,
            key=lambda x: x["score"],
            reverse=True,
        )

        return hybrid_results[:limit]