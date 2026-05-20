"""
Document Service

Handles document upload and persistence logic.
"""

import uuid

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from qdrant_client.models import (
    PointStruct,
)

from app.db.models.document import (
    Document,
)

from app.db.models.chunk import (
    Chunk,
)

from app.utils.chunking import (
    chunk_text,
)

from app.utils.file_loader import (
    save_uploaded_file,
    get_file_extension,
    load_pdf,
    load_docx,
    load_text_file,
)

from app.services.embedding_service import (
    EmbeddingService,
)

from app.services.qdrant_service import (
    QdrantService,
)


class DocumentService:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.db = db

    async def create_document(
        self,
        file_content: bytes,
        original_filename: str,
        upload_dir: str = "uploads",
    ) -> Document:
        """
        Save uploaded file
        and create database record.
        """

        file_extension = (
            get_file_extension(
                original_filename
            )
        )

        unique_filename = (
            f"{uuid.uuid4()}."
            f"{file_extension}"
        )

        file_path = save_uploaded_file(
            file_content=file_content,
            filename=unique_filename,
            upload_dir=upload_dir,
        )

        document = Document(
            filename=unique_filename,
            original_filename=(
                original_filename
            ),
            file_path=file_path,
            file_type=file_extension,
            processing_status="pending",
        )

        self.db.add(document)

        await self.db.commit()

        await self.db.refresh(document)

        return document

    async def process_document(
        self,
        document: Document,
    ):
        """
        Process document:
        - load text
        - chunk text
        - generate embeddings
        - store vectors
        - store chunk metadata
        """

        file_type = document.file_type

        if file_type == "pdf":

            text = load_pdf(
                document.file_path
            )

        elif file_type == "docx":

            text = load_docx(
                document.file_path
            )

        elif file_type == "txt":

            text = load_text_file(
                document.file_path
            )

        else:

            raise ValueError(
                "Unsupported file type"
            )

        chunks = chunk_text(text)

        embedding_service = (
            EmbeddingService()
        )

        embeddings = (
            embedding_service.encode(
                chunks
            )
        )

        qdrant_service = (
            QdrantService()
        )

        await qdrant_service.create_collection(
            dim=len(embeddings[0])
        )

        points = []

        for idx, (
            chunk,
            embedding
        ) in enumerate(
            zip(chunks, embeddings)
        ):

            point_id = str(
                uuid.uuid4()
            )

            points.append(
                PointStruct(
                    id=point_id,
                    vector=(
                        embedding.tolist()
                    ),
                    payload={
                        "document_id": document.id,
                        "document_name": document.original_filename,
                        "chunk_index": idx,
                        "text": chunk,
                    },
                )
            )

            db_chunk = Chunk(
                document_id=document.id,
                chunk_index=idx,
                text=chunk,
                qdrant_point_id=point_id,
            )

            self.db.add(db_chunk)

        await qdrant_service.upsert_points(
            points
        )

        document.processing_status = (
            "completed"
        )

        await self.db.commit()