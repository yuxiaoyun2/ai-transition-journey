from fastapi import APIRouter, Depends

from app.services.retrieval_service import RetrievalService
from app.repositories.chroma_repository import ChromaRepository
from app.repositories.document_repository import DocumentRepository
from app.services.embedding_service import EmbeddingService
from app.schemas.search_schema import SearchResponse, SearchRequest
from app.core.openai_init import get_openai_client
from app.core.config import get_settings
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


def get_retrieval_service(db: Session = Depends(get_db)) -> RetrievalService:
    settings = get_settings()
    client = get_openai_client()

    embedding_service = EmbeddingService(client=client, settings=settings)
    chroma_repository = ChromaRepository()
    document_repository = DocumentRepository(db)

    return RetrievalService(
        embedding_service=embedding_service,
        chroma_repository=chroma_repository,
        document_repository=document_repository,
        settings=settings,
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
