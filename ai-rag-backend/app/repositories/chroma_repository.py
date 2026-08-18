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
        query_embedding: list[list[float]],
        top_k: int = 3,
        document_id: int | None = None,
    ) -> dict:
        kwargs = {
            "query_embeddings": query_embedding,
            "n_results": top_k,
            "include": [
                "documents",
                "metadatas",
                "distances",
            ],
        }

        if document_id is not None:
            kwargs["where"] = {"document_id": document_id}

        return self.collection.query(**kwargs)

    def delete_by_document_id(
        self,
        document_id: int,
    ) -> None:
        self.collection.delete(
            where={
                "document_id": document_id,
            }
        )
