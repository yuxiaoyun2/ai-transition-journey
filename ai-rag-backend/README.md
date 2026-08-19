# AI RAG Backend

## Overview

This project is a RAG-based backend application built with FastAPI.

It allows users to upload PDF documents, convert document contents
into embeddings, store them in ChromaDB, and retrieve relevant
information using semantic search.

The retrieved context is used by an LLM to generate answers based on
the uploaded documents.

## Features

- PDF upload and text extraction
- Configurable text chunking with overlap
- OpenAI Embeddings integration
- Vector storage with ChromaDB
- Semantic search with Top-K retrieval
- Metadata filtering by document ID
- Distance threshold filtering
- RAG-based question answering with source information
- Document metadata persistence with SQLite
- Document deletion across SQLite, ChromaDB, and file storage
- Custom exception handling
- Application logging
- Unit tests
- Integration tests

## Architecture
```text
        Client
            │
            ▼
        FastAPI Router
            │
            ▼
        Service
    ┌──────┼──────┐
    │      │      │
    ▼      ▼      ▼
SQLite  Chroma  OpenAI
```

### Upload Flow
```text
PDF Upload
    ↓
PDF Parse
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embedding
    ↓
ChromaDB

Document Metadata
    ↓
SQLite
```

### Search / Chat Flow
```text
Question
   ↓
Embedding
   ↓
ChromaDB Semantic Search
   ↓
Top-K Chunks
   ↓
Distance Threshold
   ↓
Context
   ↓
LLM
   ↓
Answer + Sources
```

## Tech Stack

- Python
- FastAPI
- OpenAI API
- ChromaDB
- SQLite
- SQLAlchemy
- Pydantic
- pytest

## Project Structure
```text
.
├── app/
│   ├── core/
│   ├── exceptions/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   └── main.py
├── tests/
│   ├── integration/
│   ├── router/
│   ├── service/
│   └── conftest.py
├── uploads/
├── chroma_db/
├── .env.example
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/pdf/upload` | Upload and index a PDF document |
| DELETE | `/pdf/{document_id}` | Delete a document |
| POST | `/search` | Search relevant document chunks |
| POST | `/chat` | Generate an answer using RAG |


## Testing

The project includes unit and integration tests using pytest.

### Unit Tests
- Router behavior
- Service business logic
- Error handling
- Retrieval logic

### Integration Tests
- FastAPI Router → Service → Repository
- Temporary SQLite database
- Document deletion and database consistency

External dependencies such as OpenAI, ChromaDB, and the filesystem
are mocked where appropriate to keep tests isolated and reproducible.

## Error Handling

The application uses custom exceptions and centralized FastAPI
exception handlers to provide consistent HTTP error responses.

Unexpected failures are logged with stack traces for debugging.

## Design Decisions
### Dependency Injection

Services receive dependencies such as repositories, settings, and
external API clients through constructor injection.

This improves testability and makes dependencies explicit.

### UUID-based File Storage

Uploaded files are stored using UUID-based filenames while preserving
the original filename as document metadata.

This prevents files with the same original filename from overwriting
each other and helps maintain consistency across SQLite, ChromaDB,
and file storage.

### Retrieval Threshold

Semantic search results are filtered using a configurable distance
threshold before being passed to the LLM.

This reduces irrelevant context and helps prevent answers based on
unrelated document content.

## Future Improvements

- Support for complex PDF layouts
- OCR for scanned PDFs
- Improved chunking strategies
- Hybrid search
- Reranking
- Authentication and authorization
- Docker deployment
- Background processing for large documents


## Learning Outcomes

Through this project, I learned:

- How a RAG pipeline works from document ingestion to answer generation
- How embeddings and vector search are used for semantic retrieval
- How to design layered FastAPI applications
- How dependency injection improves testability
- How to separate unit and integration testing responsibilities
- How to maintain consistency across SQLite, ChromaDB, and file storage
- How to handle failures and rollback across multiple storage systems

## Key Challenges

- Maintaining consistency across SQLite, ChromaDB, and file storage
- Preventing file conflicts when uploading documents with the same filename
- Designing rollback behavior when document ingestion fails
- Distinguishing missing documents from empty semantic search results
- Keeping external dependencies testable through dependency injection