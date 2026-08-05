from fastapi import APIRouter, Depends

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.ai_service import AIService
from app.services.embedding_service import EmbeddingService
from app.repositories.chroma_repository import ChromaRepository
from app.services.retrieval_service import RetrievalService
from app.core.openai_init import get_openai_client

router = APIRouter()


def get_retrieval_service() -> RetrievalService:
    client = get_openai_client()

    embedding_service = EmbeddingService(client=client)
    chroma_repository = ChromaRepository()

    return RetrievalService(
        embedding_service=embedding_service,
        chroma_repository=chroma_repository,
    )


def get_chat_service(
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
) -> ChatService:
    client = get_openai_client()
    ai_service = AIService(client=client)

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
