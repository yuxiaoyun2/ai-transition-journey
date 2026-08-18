from openai import OpenAI, OpenAIError

from app.core.config import Settings
from app.exceptions.custom_exceptions import AIServiceError
from app.core.logger import logger


class EmbeddingService:

    def __init__(
        self,
        client: OpenAI,
        settings: Settings,
    ):
        self.client = client
        self.settings = settings

    def embeddings_create(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        try:
            response = self.client.embeddings.create(
                model=self.settings.openai_embedding_model,
                input=texts,
            )

        except OpenAIError as exc:
            logger.exception("Embedding API request failed")
            raise AIServiceError() from exc

        return [item.embedding for item in response.data]
