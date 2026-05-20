"""
Session Document Mapping
"""

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
)

from app.db.base import Base


class SessionDocument(Base):

    __tablename__ = (
        "session_documents"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    session_id = Column(
        Integer,
        ForeignKey(
            "chat_sessions.id"
        ),
    )

    document_id = Column(
        Integer,
        ForeignKey(
            "documents.id"
        ),
    )