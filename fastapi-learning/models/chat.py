from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


class ChatHistoryResponse(BaseModel):
    id: int
    user_message: str
    ai_answer: str
    created_at: str


class ChatMessageResponse(BaseModel):
    message: str
