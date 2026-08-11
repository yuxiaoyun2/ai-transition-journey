from unittest.mock import MagicMock
from app.schemas.search_schema import SearchResponse, SearchItem, ChunkMetadata
from app.services.chat_service import ChatService


def test_chat_service():
    ai_service = MagicMock()
    retrieval_service = MagicMock()

    retrieval_service.search.return_value = SearchResponse(
        question="test chat service question",
        results=[
            SearchItem(
                chunk_id="1_0",
                content="search response with mock",
                metadata=ChunkMetadata(
                    document_id=1,
                    title="test title",
                    filename="test filename",
                    page_number=1,
                    chunk_index=1,
                ),
                distance=0.5,
            )
        ],
    )

    ai_service.generate_chat.return_value = "ai service generate chat response"

    service = ChatService(
        ai_service=ai_service,
        retrieval_service=retrieval_service,
    )

    question = "test chat service question"
    top_k = 3

    result = service.chat(question=question, top_k=top_k)

    assert result.answer == "ai service generate chat response"
    assert result.sources == ["test title Page 1"]

    retrieval_service.search.assert_called_once_with(
        question=question,
        top_k=top_k,
    )

    ai_service.generate_chat.assert_called_once()
