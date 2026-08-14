from openai import OpenAI, OpenAIError

from app.core.config import get_settings
from app.exceptions.custom_exceptions import AIServiceError
from app.core.logger import logger


class EmbeddingService:

    def __init__(self, client: OpenAI):
        self.client = client

    def embeddings_create(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        try:
            settings = get_settings()

            response = self.client.embeddings.create(
                model=settings.openai_embedding_model,
                input=texts,
            )

        except OpenAIError as exc:
            logger.exception("Embedding API request failed")
            raise AIServiceError() from exc

        return [item.embedding for item in response.data]
