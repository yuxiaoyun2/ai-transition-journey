from app.repositories.chroma_repository import ChromaRepository

from app.schemas.search_schema import SearchItem, SearchResponse, ChunkMetadata

from app.services.embedding_service import (
    EmbeddingService,
)


class RetrievalService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        chroma_repository: ChromaRepository,
    ):
        self.embedding_service = embedding_service
        self.chroma_repository = chroma_repository

    def search(
        self,
        question: str,
        top_k: int = 3,
    ) -> SearchResponse:
        query_embedding = self.embedding_service.embedding_create(question)

        result = self.chroma_repository.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        ids = result.get(
            "ids",
            [[]],
        )[0]

        documents = result.get(
            "documents",
            [[]],
        )[0]

        metadatas = result.get(
            "metadatas",
            [[]],
        )[0]

        distances = result.get(
            "distances",
            [[]],
        )[0]

        items = []

        for (
            chunk_id,
            content,
            raw_metadata,
            distance,
        ) in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):
            if raw_metadata is None:
                raise ValueError("Metadataが存在しません。")

            metadata = ChunkMetadata(**raw_metadata)

            items.append(
                SearchItem(
                    chunk_id=chunk_id,
                    content=content,
                    metadata=metadata,
                    distance=distance,
                )
            )

        return SearchResponse(
            question=question,
            results=items,
        )
