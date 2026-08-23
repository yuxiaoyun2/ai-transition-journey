from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str

    openai_chat_model: str = "gpt-5-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    retrieval_top_k: int = Field(default=3, ge=1, le=10)
    retrieval_threshold: float = 0.85

    chunk_size: int = 500
    chunk_overlap: int = 100

    embedding_batch_size: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    upload_dir: str = "uploads"


@lru_cache
def get_settings() -> Settings:
    return Settings()
