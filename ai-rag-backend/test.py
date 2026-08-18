from app.repositories.chroma_repository import (
    ChromaRepository,
)

repo = ChromaRepository()

result = repo.collection.get(
    include=[
        "embeddings",
        "documents",
        "metadatas",
    ]
)

print(result)
