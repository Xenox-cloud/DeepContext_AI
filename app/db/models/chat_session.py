"""
Chat Session Model
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.db.base import Base


class ChatSession(Base):

    __tablename__ = "chat_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    session_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    title = Column(
        String,
        nullable=True,
    )