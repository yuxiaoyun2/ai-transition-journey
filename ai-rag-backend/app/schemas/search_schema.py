from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    question: str = Field(
        min_length=1,
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
    )


class SearchItem(BaseModel):
    chunk_id: str
    content: str
    metadata: dict
    distance: float


class SearchResponse(BaseModel):
    question: str
    results: list[SearchItem]
