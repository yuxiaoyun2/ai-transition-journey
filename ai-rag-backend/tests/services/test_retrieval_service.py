from unittest.mock import MagicMock

from app.services.retrieval_service import RetrievalService
from app.core.config import Settings
from app.models.document_model import Document


def test_retrieval_service():
    embedding_service = MagicMock()
    chroma_repository = MagicMock()
    document_repository = MagicMock()
    settings = MagicMock(spec=Settings)

    settings.retrieval_threshold = 1.0
    settings.retrieval_top_k = 3

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        chroma_repository=chroma_repository,
        document_repository=document_repository,
        settings=settings,
    )

    question = "search test question"
    query_embeddings = [[0.5, 0.7, 0.9]]
    top_k = 3
    document_id = 1

    embedding_service.embeddings_create.return_value = query_embeddings

    chroma_repository.search.return_value = {
        "ids": [["1_0"]],
        "documents": [["search response with mock"]],
        "metadatas": [
            [
                {
                    "document_id": 1,
                    "title": "test title",
                    "filename": "test filename",
                    "page_number": 1,
                    "chunk_index": 0,
                }
            ]
        ],
        "distances": [[0.5]],
    }

    document_repository.get_by_id.return_value = Document(
        id=1,
        title="test title",
        filename="test.pdf",
        filepath="uploads/test.pdf",
    )

    result = retrieval_service.search(
        question=question,
        top_k=top_k,
        document_id=document_id,
    )
    assert result.question == "search test question"
    assert len(result.results) == 1
    assert result.results[0].chunk_id == "1_0"
    assert result.results[0].content == ("search response with mock")
    assert result.results[0].metadata.title == ("test title")
    assert result.results[0].distance == 0.5
    assert result.message is None

    embedding_service.embeddings_create.assert_called_once_with([question])

    chroma_repository.search.assert_called_once_with(
        query_embeddings=query_embeddings,
        top_k=top_k,
        document_id=document_id,
    )

    document_repository.get_by_id.assert_called_once_with(document_id=document_id)


def test_retrieval_service_uses_settings_top_k_by_default():
    embedding_service = MagicMock()
    chroma_repository = MagicMock()
    document_repository = MagicMock()
    settings = MagicMock(spec=Settings)
    settings.retrieval_threshold = 1.0
    settings.retrieval_top_k = 7

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        chroma_repository=chroma_repository,
        document_repository=document_repository,
        settings=settings,
    )

    question = "search test question"
    query_embeddings = [[0.5, 0.7, 0.9]]
    embedding_service.embeddings_create.return_value = query_embeddings
    chroma_repository.search.return_value = {
        "ids": [[]],
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]],
    }

    result = retrieval_service.search(question=question)

    assert result.question == question
    assert result.results == []
    assert result.message == "No relevant results found."
    chroma_repository.search.assert_called_once_with(
        query_embeddings=query_embeddings,
        top_k=7,
        document_id=None,
    )


def test_retrieval_service_sets_message_when_all_results_exceed_threshold():
    embedding_service = MagicMock()
    chroma_repository = MagicMock()
    document_repository = MagicMock()
    settings = MagicMock(spec=Settings)
    settings.retrieval_threshold = 0.85
    settings.retrieval_top_k = 3

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        chroma_repository=chroma_repository,
        document_repository=document_repository,
        settings=settings,
    )

    question = "search test question"
    embedding_service.embeddings_create.return_value = [[0.5, 0.7, 0.9]]
    chroma_repository.search.return_value = {
        "ids": [["1_0"]],
        "documents": [["irrelevant search response"]],
        "metadatas": [
            [
                {
                    "document_id": 1,
                    "title": "test title",
                    "filename": "test filename",
                    "page_number": 1,
                    "chunk_index": 0,
                }
            ]
        ],
        "distances": [[0.86]],
    }

    result = retrieval_service.search(question=question)

    assert result.question == question
    assert result.results == []
    assert result.message == "No relevant results found."
