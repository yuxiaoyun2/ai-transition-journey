from openai import OpenAI, OpenAIError

from app.core.config import get_settings
from app.exceptions.custom_exceptions import AIServiceError


class EmbeddingService:

    def __init__(self, client: OpenAI):
        self.client = client

    def embeddings_create(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings = []

        for text in texts:
            embeddings.append(self.embedding_create(text))

        return embeddings

    def embedding_create(
        self,
        text: str,
    ) -> list[float]:
        try:
            settings = get_settings()
            response = self.client.embeddings.create(
                model=settings.openai_embedding_model,
                input=text,
            )
        except OpenAIError as exc:
            raise AIServiceError() from exc

        return response.data[0].embedding
