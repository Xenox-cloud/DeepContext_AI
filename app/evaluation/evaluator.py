"""
RAG Evaluation Pipeline
"""

import asyncio
import time

from app.evaluation.metrics import (
    average_latency,
    context_relevance,
    keyword_recall,
)

from app.evaluation.test_queries import (
    TEST_QUERIES
)

from app.services.rag_service import (
    RAGService
)


async def run_evaluation():

    rag_service = (
        RAGService()
    )

    recalls = []

    relevances = []

    latencies = []

    for test in TEST_QUERIES:

        start = (
            time.time()
        )

        result = await (
            rag_service.ask(
                question=(
                    test["question"]
                ),
                session_id="evaluation",
            )
        )

        latency = (
            time.time()
            -
            start
        )

        answer = (
            result["answer"]
        )

        retrieved_chunks = [
            source.get(
                "chunk",
                ""
            )
            for source in (
                result["sources"]
            )
        ]

        recall = (
            keyword_recall(
                answer=answer,
                expected_keywords=(
                    test[
                        "expected_keywords"
                    ]
                ),
            )
        )

        relevance = (
            context_relevance(
                retrieved_chunks=retrieved_chunks
            )
        )

        recalls.append(
            recall
        )

        relevances.append(
            relevance
        )

        latencies.append(
            latency
        )

        print(
            f"\nQuestion: {test['question']}"
        )

        print(
            f"Recall: {recall:.2f}"
        )

        print(
            f"Relevance: {relevance:.2f}"
        )

        print(
            f"Latency: {latency:.2f}s"
        )

    print("\n==========")

    print(
        f"Average Recall: "
        f"{sum(recalls)/len(recalls):.2f}"
    )

    print(
        f"Average Relevance: "
        f"{sum(relevances)/len(relevances):.2f}"
    )

    print(
        f"Average Latency: "
        f"{average_latency(latencies):.2f}s"
    )


if __name__ == "__main__":

    asyncio.run(
        run_evaluation()
    )