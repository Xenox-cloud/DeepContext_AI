"""
RAG Route
"""

import json

from fastapi import (
    APIRouter
)

from fastapi.responses import (
    StreamingResponse
)

from pydantic import (
    BaseModel
)

from app.schemas.rag_schema import (
    RAGResponse
)

from app.services.rag_service import (
    RAGService
)

router = APIRouter()


class AskRequest(
    BaseModel
):

    question: str

    session_id: str


@router.post(
    "/ask",
    response_model=RAGResponse,
)
async def ask_question(
    request: AskRequest,
):
    """
    RAG question answering.
    """

    rag_service = (
        RAGService()
    )

    result = await (
        rag_service.ask(
            question=request.question,
            session_id=request.session_id,
        )
    )

    return result


@router.post(
    "/ask/stream",
)
async def ask_question_stream(
    request: AskRequest,
):
    """
    Streaming RAG response.
    """

    rag_service = (
        RAGService()
    )

    async def event_generator():

        async for chunk in (
            rag_service.ask_stream(
                question=request.question,
                session_id=request.session_id,
            )
        ):

            yield (
                json.dumps(
                    {
                        "chunk": chunk
                    }
                )
                +
                "\n"
            )

    return StreamingResponse(
        event_generator(),
        media_type=(
            "application/json"
        ),
    )