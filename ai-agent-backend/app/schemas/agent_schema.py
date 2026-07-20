from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Message sent to the AI agent",
    )


class AgentChatResponse(BaseModel):
    answer: str
