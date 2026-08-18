from pydantic import ValidationError

from app.repositories.chroma_repository import ChromaRepository
from app.repositories.document_repository import DocumentRepository
from app.schemas.search_schema import SearchItem, SearchResponse, ChunkMetadata
from app.core.config import Settings
from app.services.embedding_service import (
    EmbeddingService,
)
from app.exceptions.custom_exceptions import (
    MetadataNotFoundError,
    TopkCheckError,
    RetrievalError,
    DocumentNotFoundError,
)


class RetrievalService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        chroma_repository: ChromaRepository,
        document_repository: DocumentRepository,
        settings=Settings,
    ):
        self.embedding_service = embedding_service
        self.chroma_repository = chroma_repository
        self.document_repository = document_repository
        self.settings = settings

    def search(
        self,
        question: str,
        top_k: int | None = None,
        document_id: int | None = None,
    ) -> SearchResponse:

        if top_k is None:
            top_k = self.settings.retrieval_top_k

        if top_k <= 0:
            raise TopkCheckError()

        if document_id is not None:
            document = self.document_repository.get_by_id(document_id=document_id)
            if document is None:
                raise DocumentNotFoundError()

        query_embedding = self.embedding_service.embeddings_create(question)

        result = self.chroma_repository.search(
            query_embedding=query_embedding,
            top_k=top_k,  # Top-K Retrieval
            document_id=document_id,  # Metadata Filtering
        )

        if result is None:
            raise RetrievalError()

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
                raise MetadataNotFoundError()

            try:
                metadata = ChunkMetadata(**raw_metadata)
            except ValidationError as exc:
                raise MetadataNotFoundError("Metadataの形式が不正です。") from exc

            item = SearchItem(
                chunk_id=chunk_id,
                content=content,
                metadata=metadata,
                distance=distance,
            )

            # Distance Threshold
            if item.distance <= self.settings.retrieval_threshold:
                items.append(item)

        return SearchResponse(
            question=question,
            results=items,
        )
