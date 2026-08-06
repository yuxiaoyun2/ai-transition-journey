from app.repositories.chroma_repository import ChromaRepository

from app.schemas.search_schema import SearchItem, SearchResponse, ChunkMetadata

from app.core.config import get_settings

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
        self.settings = get_settings()

    def search(
        self,
        question: str,
        top_k: int | None = None,
        document_id: int | None = None,
    ) -> SearchResponse:

        if top_k is None:
            top_k = self.settings.retrieval_top_k

        if top_k <= 0:
            raise ValueError("top_kは1以上である必要があります。")

        query_embedding = self.embedding_service.embedding_create(question)

        result = self.chroma_repository.search(
            query_embedding=query_embedding, top_k=top_k, document_id=document_id
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

        items: list[SearchItem] = []

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

            item = SearchItem(
                chunk_id=chunk_id,
                content=content,
                metadata=metadata,
                distance=distance,
            )

            if item.distance <= self.settings.retrieval_threshold:
                items.append(item)

        return SearchResponse(
            question=question,
            results=items,
        )
