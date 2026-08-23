from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    question: str = Field(
        min_length=1,
    )

    top_k: int | None = Field(
        default=None,
        ge=1,
        le=10,
    )

    document_id: int = Field(
        default=None,
        ge=1,
    )


class ChunkMetadata(BaseModel):
    document_id: int
    title: str
    filename: str
    page_number: int
    chunk_index: int


class SearchItem(BaseModel):
    chunk_id: str
    content: str
    metadata: ChunkMetadata
    distance: float


class SearchResponse(BaseModel):
    question: str
    results: list[SearchItem]
