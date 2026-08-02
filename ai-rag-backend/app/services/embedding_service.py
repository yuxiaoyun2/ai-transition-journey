from openai import OpenAI


class EmbeddingService:

    def __init__(self):
        self.client = OpenAI()

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
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        return response.data[0].embedding
