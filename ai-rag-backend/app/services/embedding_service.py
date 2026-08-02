from openai import OpenAI


class EmbeddingService:

    def __init__(self):
        self.client = OpenAI()

    def embedding_create(
        self,
        chunks: list[str],
    ) -> list[list[float]]:
        embeddings = []

        for chunk in chunks:
            embedding = (
                self.client.embeddings.create(
                    model="text-embedding-3-small", input=chunk
                )
                .data[0]
                .embedding
            )
            embeddings.append(embedding)

        return embeddings
