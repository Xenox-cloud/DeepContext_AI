from pydantic import BaseModel


class SessionResponse(
    BaseModel
):

    session_id: str

    title: str | None