from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    title: str
    content: Optional[str] = None


class DocumentResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    file_name: Optional[str]
    summary: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str


class ChatRequest(BaseModel):
    document_id: int
    question: str


class ChatResponse(BaseModel):
    answer: str


class DocumentListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[DocumentResponse]
