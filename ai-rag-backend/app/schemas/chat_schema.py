from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    top_k: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
