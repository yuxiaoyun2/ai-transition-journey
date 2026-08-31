from fastapi import APIRouter, Depends

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.ai_service import AIService
from app.services.embedding_service import EmbeddingService
from app.repositories.chroma_repository import ChromaRepository
from app.repositories.document_repository import DocumentRepository
from app.services.retrieval_service import RetrievalService
from app.core.openai_init import get_openai_client
from app.core.config import get_settings
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


def get_retrieval_service(db: Session = Depends(get_db)) -> RetrievalService:
    client = get_openai_client()
    settings = get_settings()

    embedding_service = EmbeddingService(client=client, settings=settings)
    chroma_repository = ChromaRepository()
    document_repository = DocumentRepository(db)

    return RetrievalService(
        embedding_service=embedding_service,
        chroma_repository=chroma_repository,
        document_repository=document_repository,
        settings=settings,
    )


def get_chat_service(
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
) -> ChatService:
    client = get_openai_client()
    settings = get_settings()
    ai_service = AIService(client=client, settings=settings)

    return ChatService(ai_service=ai_service, retrieval_service=retrieval_service)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    return service.chat(question=request.question, top_k=request.top_k)
