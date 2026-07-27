DOCUMENTS = {
    "openai": "OpenAI develops artificial intelligence models.",
    "fastapi": "FastAPI is a modern web framework for Python.",
    "rag": "RAG combines retrieval and generation.",
}


class DocumentRepository:
    def search(self, keyword: str) -> str | None:
        keyword = keyword.lower()

        for value in DOCUMENTS.values():
            if keyword in value.lower():
                return value

        return None
