"""Hybrid retrieval tests. No models, Qdrant or Groq needed: those are replaced with fakes.

Run: pytest
"""
import asyncio
from types import SimpleNamespace

import numpy as np

from app.services.hybrid_search_service import HybridSearchService
from app.services.reranker_service import RerankerService


class FakeEmbedder:
    def encode(self, texts):
        return np.ones((len(texts), 4), dtype="float32")


class FakeQdrantClient:
    def __init__(self, points):
        self.points = points
        self.last_kwargs = None

    async def query_points(self, **kwargs):
        self.last_kwargs = kwargs
        return SimpleNamespace(points=self.points)


def make_service(points):
    svc = HybridSearchService.__new__(HybridSearchService)  # skip loading real models
    svc.embedding_service = FakeEmbedder()
    svc.qdrant_service = SimpleNamespace(client=FakeQdrantClient(points), collection_name="documents")
    return svc


def point(score, text, doc_id=1):
    return SimpleNamespace(score=score, payload={"text": text, "document_id": doc_id})


def test_keyword_score_is_bounded_and_ignores_repetition():
    score = HybridSearchService.keyword_score
    assert score("vector database", "a vector database stores vectors") == 1.0
    assert score("vector database", "vector " * 50) == 0.5  # repeats don't inflate the score
    assert score("Qdrant?", "We use qdrant.") == 1.0  # punctuation and case ignored
    assert score("", "anything") == 0.0


def test_repeated_keyword_cannot_outrank_strong_semantic_match():
    # The old raw word count gave the spammy chunk 0.3 * 40 = 12 points and put it first
    svc = make_service([
        point(0.92, "Transformers use self-attention to weigh tokens"),
        point(0.20, "attention " * 40),
    ])
    results = asyncio.run(svc.search("how does attention work", limit=2))
    assert results[0]["text"].startswith("Transformers")
    assert all(0 <= r["keyword_score"] <= 1 for r in results)


def test_session_documents_are_filtered_inside_qdrant():
    svc = make_service([point(0.8, "chunk", doc_id=7)])
    asyncio.run(svc.search("q", limit=5, document_ids=[7, 9]))
    query_filter = svc.qdrant_service.client.last_kwargs["query_filter"]
    condition = query_filter.must[0]
    assert condition.key == "document_id"
    assert condition.match.any == [7, 9]


def test_no_filter_without_session_documents():
    svc = make_service([])
    asyncio.run(svc.search("q", limit=5))
    assert svc.qdrant_service.client.last_kwargs["query_filter"] is None


def test_reranker_handles_empty_candidates():
    reranker = RerankerService.__new__(RerankerService)  # no model needed for the empty case
    assert reranker.rerank("q", []) == []
