"""
Evaluation Test Queries
"""

TEST_QUERIES = [
    {
        "question": (
            "What is self-attention?"
        ),
        "expected_keywords": [
            "query",
            "key",
            "value",
            "attention",
        ],
    },
    {
        "question": (
            "Difference between positional encoding and self-attention"
        ),
        "expected_keywords": [
            "position",
            "sequence",
            "attention",
            "context",
        ],
    },
    {
        "question": (
            "What are transformers?"
        ),
        "expected_keywords": [
            "attention",
            "encoder",
            "decoder",
        ],
    },
]