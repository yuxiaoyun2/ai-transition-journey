from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    session_id: str = Field(
        min_length=1,
        max_length=100,
    )
    message: str = Field(
        min_length=1,
    )


class AgentChatResponse(BaseModel):
    answer: str
    source: str


class SearchResult(BaseModel):
    answer: str = Field(description="The final response to the user.")
    source: str = Field(
        description="The document name or tool name used to generate the answer."
    )
