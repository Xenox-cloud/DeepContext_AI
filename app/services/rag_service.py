"""
RAG Service
"""

import time

from sqlalchemy import (
    select
)

from groq import (
    AsyncGroq
)

from app.core.chat_memory import (
    chat_memory
)

from app.core.config import (
    settings
)

from app.core.logging import (
    logger
)

from app.db.models.chat_session import (
    ChatSession
)

from app.prompts.rag_prompts import (
    SYSTEM_PROMPT,
    build_user_prompt,
)

from app.services.hybrid_search_service import (
    HybridSearchService
)

from app.services.reranker_service import (
    RerankerService
)

from app.services.session_service import (
    SessionService
)


class RAGService:

    def __init__(self):

        self.hybrid_search_service = (
            HybridSearchService()
        )

        self.reranker_service = (
            RerankerService()
        )

        self.client = AsyncGroq(
            api_key=settings.groq_api_key
        )

    async def _get_context(
        self,
        question: str,
        session_id: str,
        limit: int = 10,
        db=None,
    ):

        retrieval_start = (
            time.time()
        )

        logger.info(
            "Retrieval started",
            session_id=session_id,
        )

        sources = []

        document_ids = None

        if db:

            session_service = (
                SessionService(db)
            )

            stmt = select(
                ChatSession
            ).where(
                ChatSession.session_id
                ==
                session_id
            )

            result = await (
                db.execute(stmt)
            )

            session = (
                result.scalar_one_or_none()
            )

            if session:

                document_ids = await (
                    session_service
                    .get_session_document_ids(
                        session.id
                    )
                )

        results = await (
            self.hybrid_search_service.search(
                query=question,
                limit=limit,
                document_ids=document_ids,
            )
        )

        chunk_source_pairs = []

        for point in results:

            payload = (
                point["payload"]
            )

            text = (
                point["text"]
            )

            if text:

                chunk_source_pairs.append(
                    {
                        "text": text,
                        "source": {
                            "document": (
                                payload.get(
                                    "document_name"
                                )
                            ),
                            "chunk_index": (
                                payload.get(
                                    "chunk_index"
                                )
                            ),
                        },
                    }
                )

        reranked = (
            self.reranker_service.rerank(
                query=question,
                documents=[
                    pair["text"]
                    for pair in chunk_source_pairs
                ],
                top_k=5,
            )
        )

        reranked_chunks = []

        for reranked_doc in reranked:

            reranked_text = (
                reranked_doc[0]
            )

            for pair in (
                chunk_source_pairs
            ):

                if (
                    reranked_text
                    ==
                    pair["text"]
                ):

                    reranked_chunks.append(
                        {
                            "text": (
                                reranked_text
                            ),
                            "source": (
                                pair["source"]
                            ),
                        }
                    )

                    break

        formatted_chunks = []

        final_sources = []

        for item in (
            reranked_chunks
        ):

            chunk = (
                item["text"]
            )

            source = (
                item["source"]
            )

            final_sources.append(
                {
                    "document": (
                        source["document"]
                    ),
                    "chunk_index": (
                        source["chunk_index"]
                    ),
                    "chunk": (
                        chunk
                    ),
                }
            )

            formatted_chunks.append(
                f"""
        [Source: {source['document']} | Chunk {source['chunk_index']}]

        {chunk}
        """
            )

        context = "\n\n".join(
            formatted_chunks
        )

        retrieval_time = (
            time.time()
            -
            retrieval_start
        )

        logger.info(
            "Retrieval completed",
            session_id=session_id,
            retrieval_time=(
                round(
                    retrieval_time,
                    2,
                )
            ),
            chunks_retrieved=(
                len(
                    reranked_chunks
                )
            ),
        )

        return (
            context,
            final_sources,
        )

    async def ask(
        self,
        question: str,
        session_id: str,
        limit: int = 10,
        db=None,
    ):

        request_start = (
            time.time()
        )

        logger.info(
            "RAG request started",
            session_id=session_id,
        )

        try:

            if not question.strip():

                return {
                    "question": (
                        question
                    ),
                    "answer": (
                        "Question cannot be empty."
                    ),
                    "sources": [],
                }

            context, sources = await (
                self._get_context(
                    question=question,
                    session_id=session_id,
                    limit=limit,
                    db=db,
                )
            )

            history = (
                chat_memory.get_messages(
                    session_id
                )
            )

            messages = [
                {
                    "role": "system",
                    "content": (
                        SYSTEM_PROMPT
                    ),
                }
            ]

            messages.extend(
                history
            )

            messages.append(
                {
                    "role": "user",
                    "content": (
                        build_user_prompt(
                            context=context,
                            question=question,
                        )
                    ),
                }
            )

            llm_start = (
                time.time()
            )

            response = await (
                self.client.chat.completions.create(
                    model=(
                        "llama-3.3-70b-versatile"
                    ),
                    messages=messages,
                    temperature=0.3,
                )
            )

            llm_time = (
                time.time()
                -
                llm_start
            )

            logger.info(
                "LLM response completed",
                session_id=session_id,
                llm_time=(
                    round(
                        llm_time,
                        2,
                    )
                ),
            )

            answer = (
                response
                .choices[0]
                .message.content
            )

            chat_memory.add_message(
                session_id=session_id,
                role="user",
                content=question,
            )

            chat_memory.add_message(
                session_id=session_id,
                role="assistant",
                content=answer,
            )

            total_time = (
                time.time()
                -
                request_start
            )

            logger.info(
                "RAG request completed",
                session_id=session_id,
                total_time=(
                    round(
                        total_time,
                        2,
                    )
                ),
            )

            return {
                "question": (
                    question
                ),
                "answer": (
                    answer
                ),
                "sources": (
                    sources
                ),
            }

        except Exception:

            logger.exception(
                "RAG pipeline failed"
            )

            raise

    async def ask_stream(
        self,
        question: str,
        session_id: str,
        limit: int = 10,
        db=None,
    ):

        request_start = (
            time.time()
        )

        logger.info(
            "Streaming RAG request started",
            session_id=session_id,
        )

        try:

            if not question.strip():

                yield (
                    "Question cannot be empty."
                )

                return

            context, sources = await (
                self._get_context(
                    question=question,
                    session_id=session_id,
                    limit=limit,
                    db=db,
                )
            )

            history = (
                chat_memory.get_messages(
                    session_id
                )
            )

            messages = [
                {
                    "role": "system",
                    "content": (
                        SYSTEM_PROMPT
                    ),
                }
            ]

            messages.extend(
                history
            )

            messages.append(
                {
                    "role": "user",
                    "content": (
                        build_user_prompt(
                            context=context,
                            question=question,
                        )
                    ),
                }
            )

            stream = await (
                self.client.chat.completions.create(
                    model=(
                        "llama-3.3-70b-versatile"
                    ),
                    messages=messages,
                    temperature=0.3,
                    stream=True,
                )
            )

            full_answer = ""

            async for chunk in stream:

                content = (
                    chunk.choices[0]
                    .delta.content
                )

                if content:

                    full_answer += (
                        content
                    )

                    yield content

            chat_memory.add_message(
                session_id=session_id,
                role="user",
                content=question,
            )

            chat_memory.add_message(
                session_id=session_id,
                role="assistant",
                content=full_answer,
            )

            total_time = (
                time.time()
                -
                request_start
            )

            logger.info(
                "Streaming RAG completed",
                session_id=session_id,
                total_time=(
                    round(
                        total_time,
                        2,
                    )
                ),
            )

        except Exception:

            logger.exception(
                "Streaming RAG pipeline failed"
            )

            raise