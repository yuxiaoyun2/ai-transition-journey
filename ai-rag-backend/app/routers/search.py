from fastapi import APIRouter, Depends

from app.services.retrieval_service import RetrievalService
from app.repositories.chroma_repository import ChromaRepository
from app.services.embedding_service import EmbeddingService
from app.schemas.search_schema import SearchResponse, SearchRequest

router = APIRouter()


def get_retrieval_service() -> RetrievalService:
    embedding_service = EmbeddingService()
    chroma_repository = ChromaRepository()

    return RetrievalService(
        embedding_service,
        chroma_repository,
    )


@router.post("", response_model=SearchResponse)
def search_documents(
    request: SearchRequest,
    service: RetrievalService = Depends(get_retrieval_service),
):
    return service.search(
        question=request.question,
        top_k=request.top_k,
    )
