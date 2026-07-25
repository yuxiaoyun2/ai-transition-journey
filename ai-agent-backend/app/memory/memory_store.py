from app.memory.memory import ConversationMemory


class MemoryStore:
    def __init__(self):
        self._memories: dict[str, ConversationMemory] = {}

    def get_memory(self, session_id: str) -> ConversationMemory:
        if session_id not in self._memories:
            self._memories[session_id] = ConversationMemory()

        return self._memories[session_id]

    def delete_memory(self, session_id: str) -> None:
        self._memories.pop(session_id, None)


memory_store = MemoryStore()
