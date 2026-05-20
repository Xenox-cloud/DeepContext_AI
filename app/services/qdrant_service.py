"""
Qdrant Service
"""

from typing import List

from qdrant_client import (
    AsyncQdrantClient,
)

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from app.core.config import settings


class QdrantService:

    def __init__(self):

        self.client = AsyncQdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            check_compatibility=False,
        )

        self.collection_name = (
            settings.qdrant_collection_name
        )

    async def create_collection(
        self,
        dim: int,
    ):

        collections = (
            await self.client.get_collections()
        )

        existing = [
            c.name
            for c in collections.collections
        ]

        if self.collection_name in existing:
            return

        await self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=dim,
                distance=Distance.COSINE,
            ),
        )

    async def upsert_points(
        self,
        points: List[PointStruct],
    ):

        await self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )