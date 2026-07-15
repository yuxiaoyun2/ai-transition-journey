# AI Document Assistant Backend

## Overview

AI Document Assistant Backend is a RESTful API built with FastAPI.

Users can upload PDF documents, search documents, summarize content using OpenAI, and ask questions based on uploaded documents.

The project focuses on maintainable architecture, automated testing, containerization, and CI/CD practices.


## Features

- PDF document upload and text extraction
- Document CRUD operations
- Keyword-based document search
- Pagination
- AI-powered document summarization
- AI-powered question answering based on document content
- Global exception handling
- Centralized logging
- Unit and API tests
- Docker support
- Docker Compose support
- GitHub Actions CI


## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- OpenAI API
- Pydantic
- PyPDF
- pytest
- Docker
- Docker Compose
- GitHub Actions

## Architecture

```text
Client
  │
  ▼
FastAPI Router
  │
  ▼
Document Service / AI Client
  │
  ▼
Repository Layer
  │
  ▼
SQLite
```

The project follows a layered architecture (Router → Service → Repository) to improve maintainability, testability, and separation of responsibilities.

## Project Structure

```text
ai-document-assistant-backend/
├── app/
│   ├── ai/
│   ├── exceptions/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── dependencies.py
│   ├── database.py
│   └── main.py
├── tests/
├── uploads/
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## API Endpoints

| Method | Endpoint                   | Description                        |
| ------ | -------------------------- | ---------------------------------- |
| POST   | `/documents`               | Create a document                  |
| GET    | `/documents`               | List documents with pagination     |
| GET    | `/documents/search`        | Search documents by keyword        |
| GET    | `/documents/{document_id}` | Get a document by ID               |
| DELETE | `/documents/{document_id}` | Delete a document                  |
| POST   | `/documents/upload`        | Upload and process a PDF document  |
| POST   | `/documents/chat`          | Ask a question based on a document |

Interactive API documentation is available at:

http://localhost:8000/docs

## Getting Started

1. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install development dependencies
```bash
python -m pip install -r requirements-dev.txt
```

3. Configure environment variables
```bash
OPENAI_API_KEY=your_openai_api_key
```

4. Run the application
```bash
python -m uvicorn app.main:app --reload
```

Open:
```text
http://localhost:8000/docs
```


## Docker

Build the image:
```bash
docker build -t ai-document-assistant-backend .
```

Run the container:
```bash
docker run \
  --name ai-document-api \
  -p 8000:8000 \
  --env-file .env \
  ai-document-assistant-backend
```

## Docker Compose

Start the application:
```bash
docker compose up --build
```

Run in the background:
```bash
docker compose up -d --build
```

Stop and remove the Compose containers:
```bash
docker compose down
```

## Testing

Run all tests:
```bash
python -m pytest -v
```

Check code formatting:
```bash
python -m black --check .
```

The test suite uses:

FastAPI TestClient
pytest fixtures
MagicMock
patch
mocked OpenAI responses

External OpenAI API calls are not performed during unit tests.

## CI

GitHub Actions automatically runs Black and pytest on every push to the main branch.

```text
Install dependencies
  ↓
Black formatting check
  ↓
pytest
```

The workflow is defined in:
```text
.github/workflows/ai-document-ci.yml
```

## Future Improvements

- PostgreSQL and pgvector integration
- Retrieval-Augmented Generation (RAG)
- JWT-based authentication and authorization
- Asynchronous document processing
- Background job processing for large PDF files