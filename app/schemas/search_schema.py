from pydantic import BaseModel


class SearchResult(
    BaseModel
):

    document_id: int | None

    chunk_index: int | None

    text: str

    score: float


class SearchResponse(
    BaseModel
):

    query: str

    results: list[
        SearchResult
    ]