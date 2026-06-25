from pydantic import BaseModel
from typing import Optional


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


class ChatSummaryResponse(BaseModel):
    summary: str


class ChatStatsResponse(BaseModel):
    total_messages: int
    total_summaries: int
    latest_chat_time: Optional[str] = None
