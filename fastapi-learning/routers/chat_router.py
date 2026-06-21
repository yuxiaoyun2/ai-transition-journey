from fastapi import APIRouter, HTTPException

from models.chat import ChatRequest, ChatResponse
from services.chat_service import generate_answer

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
