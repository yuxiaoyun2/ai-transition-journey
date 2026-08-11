from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.schemas.search_schema import SearchResponse, SearchItem, ChunkMetadata
from app.routers.search import get_retrieval_service

client = TestClient(app)


def test_search_router():
    mock_service = MagicMock()

    mock_service.search.return_value = SearchResponse(
        question="search test",
        results=[
            SearchItem(
                chunk_id="1_0",
                content="test content",
                metadata=ChunkMetadata(
                    document_id=1,
                    title="test title",
                    filename="test filename",
                    page_number=1,
                    chunk_index=0,
                ),
                distance=0.5,
            )
        ],
    )

    def override_retrieval_service():
        return mock_service

    app.dependency_overrides[get_retrieval_service] = override_retrieval_service

    try:
        response = client.post(
            "/search", json={"question": "search test", "top_k": 3, "document_id": 1}
        )

        assert response.status_code == 200

        data = response.json()
        assert data["question"] == "search test"
        assert len(data["results"]) == 1
        assert data["results"][0]["chunk_id"] == "1_0"
        assert data["results"][0]["content"] == "test content"
        assert data["results"][0]["metadata"]["title"] == "test title"
        assert data["results"][0]["metadata"]["filename"] == "test filename"
        assert data["results"][0]["distance"] == 0.5

        mock_service.search.assert_called_once_with(
            question="search test",
            top_k=3,
            document_id=1,
        )

        assert response.headers["content-type"].startswith("application/json")
    finally:
        app.dependency_overrides.pop(get_retrieval_service, None)
