"""
Chat Memory Service
"""

from collections import defaultdict


class ChatMemoryService:

    def __init__(self):

        self.memory = defaultdict(
            list
        )

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):

        self.memory[
            session_id
        ].append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_messages(
        self,
        session_id: str,
    ):

        return self.memory.get(
            session_id,
            [],
        )

    def clear_memory(
        self,
        session_id: str,
    ):

        self.memory[
            session_id
        ] = []