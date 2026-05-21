"""
Search Route
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue,
)

from app.api.dependencies import (
    get_db
)

from app.db.models.document import (
    Document
)

from app.schemas.search_schema import (
    SearchResponse
)

from app.services.embedding_service import (
    EmbeddingService
)

from app.services.qdrant_service import (
    QdrantService
)

router = APIRouter()


@router.get(
    "/search",
    response_model=SearchResponse,
)
async def semantic_search(
    query: str = Query(
        ...
    ),
    limit: int = Query(
        5
    ),
    document_id: int | None = Query(
        None
    ),
    db: AsyncSession = Depends(
        get_db
    ),
):
    """
    Semantic vector search.
    """

    if not query.strip():

        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty",
        )

    embedding_service = (
        EmbeddingService()
    )

    qdrant_service = (
        QdrantService()
    )

    query_embedding = (
        embedding_service.encode(
            [query]
        )[0]
    )

    if len(query_embedding) == 0:

        raise HTTPException(
            status_code=500,
            detail=(
                "Embedding generation failed"
            ),
        )

    search_filter = None

    if document_id is not None:

        search_filter = Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(
                        value=document_id
                    ),
                )
            ]
        )

    results = await (
        qdrant_service.client.query_points(
            collection_name=(
                qdrant_service.collection_name
            ),
            query=(
                query_embedding.tolist()
            ),
            query_filter=search_filter,
            limit=limit,
        )
    )

    formatted_results = []

    for point in results.points:

        payload = (
            point.payload
        )

        current_document_id = (
            payload.get(
                "document_id"
            )
        )

        stmt = select(
            Document
        ).where(
            Document.id
            ==
            current_document_id
        )

        result = await db.execute(
            stmt
        )

        document = (
            result.scalar_one_or_none()
        )

        formatted_results.append(
            {
                "document_id": (
                    document.id
                    if document
                    else None
                ),
                "chunk_index": (
                    payload.get(
                        "chunk_index"
                    )
                ),
                "text": (
                    payload.get(
                        "text"
                    )
                ),
                "score": (
                    float(
                        point.score
                    )
                ),
            }
        )

    return {
        "query": query,
        "results": (
            formatted_results
        ),
    }