import chromadb


class ChromaRepository:

    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")

        self.collection = self.client.get_or_create_collection("pdf")

    def insert(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        chunks: list[str],
        metadatas: list[dict],
    ):

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )

        return True

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3,
    ) -> dict:
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )
