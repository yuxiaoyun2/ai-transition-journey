from fastapi import APIRouter, Depends

from app.services.retrieval_service import RetrievalService
from app.repositories.chroma_repository import ChromaRepository
from app.services.embedding_service import EmbeddingService
from app.schemas.search_schema import SearchResponse, SearchRequest
from app.core.openai_init import get_openai_client
from app.core.config import get_settings

router = APIRouter()

client = get_openai_client()


def get_retrieval_service() -> RetrievalService:
    embedding_service = EmbeddingService(client=client)
    chroma_repository = ChromaRepository()
    settings = get_settings()

    return RetrievalService(
        embedding_service,
        chroma_repository,
        settings,
    )


@router.post("", response_model=SearchResponse)
def search_documents(
    request: SearchRequest,
    service: RetrievalService = Depends(get_retrieval_service),
):
    return service.search(
        question=request.question,
        top_k=request.top_k,
        document_id=request.document_id,
    )
