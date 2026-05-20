"""
Chunk Database Model
"""

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class Chunk(Base):

    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    qdrant_point_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    document = relationship(
        "Document",
        back_populates="chunks",
    )