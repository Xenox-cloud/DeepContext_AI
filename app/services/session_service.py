"""
Session Service
"""

import uuid

from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.db.models.chat_session import (
    ChatSession
)

from app.db.models.session_document import (
    SessionDocument
)


class SessionService:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.db = db

    async def create_session(
        self,
        title: str = "New Chat",
    ):

        session = ChatSession(
            session_id=str(
                uuid.uuid4()
            ),
            title=title,
        )

        self.db.add(session)

        await self.db.commit()

        await self.db.refresh(
            session
        )

        return session

    async def attach_document(
        self,
        session_db_id: int,
        document_id: int,
    ):

        mapping = SessionDocument(
            session_id=session_db_id,
            document_id=document_id,
        )

        self.db.add(mapping)

        await self.db.commit()

        return mapping

    async def get_session_documents(
        self,
        session_db_id: int,
    ):

        stmt = select(
            SessionDocument
        ).where(
            SessionDocument.session_id
            ==
            session_db_id
        )

        result = await (
            self.db.execute(stmt)
        )

        return (
            result.scalars().all()
        )
    
    async def get_session_document_ids(
        self,
        session_db_id: int,
    ):

        mappings = await (
            self.get_session_documents(
                session_db_id
            )
        )

        return [
            mapping.document_id
            for mapping in mappings
        ]