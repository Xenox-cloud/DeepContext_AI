from pydantic import BaseModel


class SourceChunk(
    BaseModel
):

    document: str | None

    chunk_index: int | None


class RAGResponse(
    BaseModel
):

    question: str

    answer: str

    sources: list[
        SourceChunk
    ]