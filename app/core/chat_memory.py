"""
Global Chat Memory
"""

from app.services.chat_memory_service import (
    ChatMemoryService,
)

chat_memory = (
    ChatMemoryService()
)