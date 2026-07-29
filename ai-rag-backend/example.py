import chromadb

client = chromadb.Client()

collection = client.create_collection("documents")

collection.add(ids=["1"], documents=["Python is a programming language."])

result = collection.query(query_texts=["What is Python?"], n_results=1)

print(result)
