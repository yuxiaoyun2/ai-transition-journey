from fastapi import APIRouter, HTTPException

from models.chat import (
    ChatRequest,
    ChatResponse,
    ChatHistoryResponse,
    ChatMessageResponse,
    ChatSummaryResponse,
    ChatStatsResponse,
)
from services.chat_service import (
    generate_answer,
    get_chat_history,
    delete_chat_history,
    generate_summary,
    get_chat_stats,
)

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    answer = generate_answer(request.message)

    return {"answer": answer}


@router.get(
    "/chat/history",
    response_model=list[ChatHistoryResponse],
)
def chat_history():
    return get_chat_history()


@router.delete(
    "/chat/history",
    response_model=ChatMessageResponse,
)
def delete_chat_history_api():
    deleted = delete_chat_history()

    if not deleted:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return {"message": "All chat history deleted"}


@router.post(
    "/chat/summary",
    response_model=ChatSummaryResponse,
)
def chat_summary():
    return generate_summary()


@router.get(
    "/chat/stats",
    response_model=ChatStatsResponse,
)
def chat_stats():
    return get_chat_stats()
