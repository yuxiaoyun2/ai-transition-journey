import chromadb
from openai import OpenAI

client = OpenAI()

embedding = (
    client.embeddings.create(
        model="text-embedding -3-small", input="Python is a programming language."
    )
    .data[0]
    .embedding
)

db = chromadb.PersistentClient(path="./chroma_db")

collection = db.get_or_create_collection("documents")

collection.add(
    ids=["1"],
    embeddings=[embedding],
    documents=["Python is a programming language."],
    metadatas=[{"source": "sample"}],
)

print("Saved.")
