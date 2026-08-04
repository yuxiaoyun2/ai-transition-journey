from openai import OpenAI

from app.core.config import get_settings


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
        settings = get_settings()
        response = self.client.embeddings.create(
            model=settings.openai_embedding_model,
            input=text,
        )

        return response.data[0].embedding
