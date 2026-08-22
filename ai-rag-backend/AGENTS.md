# AGENTS.md

## Project Overview

This repository is a synchronous FastAPI backend for retrieval-augmented generation over uploaded PDFs.

The main workflow is:

1. Save an uploaded PDF using a UUID-based filename.
2. Extract and chunk text by page.
3. Generate embeddings with OpenAI.
4. Store chunks and metadata in ChromaDB.
5. Store document metadata in SQLite.
6. Retrieve relevant chunks and use them as context for chat responses.

Local runtime data in `uploads/`, `chroma_db/`, and `rag.db` must not be committed.

## Architecture

- `app/main.py`: constructs the FastAPI application and registers routers and exception handlers.
- `app/routers/`: handles HTTP transport and dependency wiring. Keep business logic out of routers.
- `app/schemas/`: defines Pydantic API and Chroma metadata contracts.
- `app/services/`: owns business workflows and coordinates repositories and external APIs.
- `app/repositories/`: encapsulates SQLite and ChromaDB persistence.
- `app/models/`: contains SQLAlchemy models.
- `app/core/`: contains configuration, logging, and shared client initialization.
- `app/exceptions/`: defines application exceptions and their HTTP mappings.
- `tests/router/`: verifies HTTP contracts and dependency wiring.
- `tests/services/`: verifies business logic in isolation.
- `tests/integration/`: verifies workflows across multiple layers.

Dependencies should point inward: routers compose services, services use repositories, and repositories must not depend on routers or services.

## Coding Conventions

- Follow existing Python style and format changed Python files with Black.
- Add type hints to public functions and non-obvious data structures.
- Use constructor injection for repositories, settings, and external clients.
- Keep router handlers thin and preserve declared response models.
- Use Pydantic models at API and persisted metadata boundaries.
- Read configuration through `Settings` or `get_settings()` rather than hard-coding configurable values.
- Use the shared logger from `app.core.logger`; do not add `print` calls to application code.
- Preserve UUID-based stored filenames and retain original filenames only as metadata.

## Error Handling and Data Consistency

- Use an `AppError` subclass for expected application or external-service failures.
- Register new application exceptions in `app/exceptions/handlers.py` with an explicit HTTP status.
- Preserve exception causes with `raise ... from exc` when translating lower-level errors.
- Log unexpected operational failures with stack traces.
- Do not suppress broad exceptions. Catch them only when performing cleanup or adding context, then re-raise.
- Upload and deletion workflows span the filesystem, SQLite, and ChromaDB. Changes must preserve consistency and clean up partial writes when an operation fails.
- Treat a missing document as an error and an empty retrieval result as a valid outcome.
- Preserve retrieval semantics: results qualify when their distance is less than or equal to the configured threshold.

## Testing

Run the full test suite from the repository root:

```bash
python -m pytest -q
```

For behavioral changes:

- Add or update service tests for business rules and failure paths.
- Add router tests for request validation, response contracts, status codes, or exception mappings.
- Add integration tests for workflows spanning multiple persistence layers.
- Mock OpenAI, ChromaDB, and filesystem operations in unit tests.
- Use temporary storage for persistence tests; tests must not mutate local runtime data.
- Assert rollback behavior when changing upload or deletion workflows.

## Rules for Making Changes

- Inspect all affected layers and their tests before changing a workflow.
- Make the smallest coherent change and preserve layer boundaries.
- Update schemas, tests, and documentation when changing endpoint contracts.
- Treat `ChunkMetadata` changes as persisted-data contract changes.
- Treat SQLAlchemy model changes as database schema changes. `create_all()` does not migrate existing tables.
- Do not modify or delete local runtime data unless explicitly requested.
- Never commit `.env`, credentials, uploaded files, databases, vector stores, caches, or virtual environments.
- Preserve unrelated working-tree changes.

## Dependency Management

- Declare every directly imported third-party package in `requirements.txt`.
- Avoid new dependencies when the standard library or an existing package is sufficient.
- Remove dependencies only after confirming they are unused by application code and tests.
- Run the full test suite after dependency upgrades, especially for FastAPI, Pydantic, SQLAlchemy, OpenAI, and ChromaDB.
- Keep `.env.example`, `requirements.txt`, and README setup instructions synchronized with configuration and dependency changes.
