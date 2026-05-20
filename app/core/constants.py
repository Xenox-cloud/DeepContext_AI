"""
Application Constants

Defines constants used throughout the application.
"""

# Collection names
COLLECTION_NAME = "documents"

# Embedding dimensions (BAAI/bge-large-en-v1.5)
EMBEDDING_DIMENSIONS = 1024

# Chunk sizes
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

# Document types
SUPPORTED_DOCUMENT_TYPES = ["txt", "pdf", "docx", "xlsx", "csv"]

# API limits
MAX_BATCH_SIZE = 100
MAX_SEARCH_RESULTS = 50

# Processing timeouts
DOCUMENT_PROCESSING_TIMEOUT = 300  # seconds
SEARCH_TIMEOUT = 60  # seconds
