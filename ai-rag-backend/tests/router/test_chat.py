from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.schemas.chat_schema import ChatResponse
from app.routers.chat import get_chat_service
from app.exceptions.custom_exceptions import AIServiceError

client = TestClient(app)


def test_chat_router():
    chat_service = MagicMock()

    chat_service.chat.return_value = ChatResponse(
        answer="test answer",
        sources=["sample.pdf Page 1"],
    )

    def override_chat_service():
        return chat_service

    app.dependency_overrides[get_chat_service] = override_chat_service

    try:
        response = client.post(
            "/chat",
            json={
                "question": "test question",
                "top_k": 3,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["answer"] == "test answer"
        assert data["sources"][0] == "sample.pdf Page 1"

        chat_service.chat.assert_called_once_with(
            question="test question",
            top_k=3,
        )

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )


def test_ai_service_error():
    chat_service = MagicMock()

    chat_service.chat.side_effect = AIServiceError()

    def override_chat_service():
        return chat_service

    app.dependency_overrides[get_chat_service] = override_chat_service

    try:
        response = client.post(
            "/chat",
            json={
                "question": "test question",
                "top_k": 3,
            },
        )

        assert response.status_code == 503

        assert response.json() == {"error": ("AI service is currently unavailable")}

    finally:
        app.dependency_overrides.pop(
            get_chat_service,
            None,
        )
