from fastapi import APIRouter, HTTPException

from models.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from services.chat_service import generate_answer, get_chat_history

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    try:
        answer = generate_answer(request.message)
        return {"answer": answer}

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate AI response",
        )


@router.get("/chat/history", response_model=list[ChatHistoryResponse])
def chat_history():
    return get_chat_history()
