"""
Evaluation Metrics
"""

from typing import (
    List
)


def keyword_recall(
    answer: str,
    expected_keywords: List[str],
):

    answer_lower = (
        answer.lower()
    )

    matches = 0

    for keyword in (
        expected_keywords
    ):

        if (
            keyword.lower()
            in
            answer_lower
        ):

            matches += 1

    return (
        matches
        /
        len(expected_keywords)
    )


def context_relevance(
    retrieved_chunks: List[str],
):

    if not retrieved_chunks:

        return 0

    total_chars = sum(
        len(chunk)
        for chunk in retrieved_chunks
    )

    useful_chunks = sum(
        1
        for chunk in retrieved_chunks
        if len(chunk.strip()) > 100
    )

    return (
        useful_chunks
        /
        len(retrieved_chunks)
    )


def average_latency(
    latencies: List[float]
):

    if not latencies:

        return 0

    return (
        sum(latencies)
        /
        len(latencies)
    )