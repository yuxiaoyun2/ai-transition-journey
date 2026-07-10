from unittest.mock import MagicMock

import pytest

from app.exceptions.custom_exceptions import (
    DocumentContentEmptyError,
    DocumentNotFoundError,
)
from app.models.document import Document
from app.schemas.document import ChatRequest
from app.services.document_service import DocumentService


def test_chat_with_doc_success():
    repository = MagicMock()
    ai_client = MagicMock()

    document = Document(
        id=1,
        title="Test Document",
        content="契約期間は1年間です。",
    )

    repository.find_by_id.return_value = document
    ai_client.generate_chat.return_value = "契約期間は1年間です。"

    service = DocumentService(repository, ai_client)

    request = ChatRequest(
        document_id=1,
        question="契約期間は？",
    )

    result = service.chat_with_doc(request)

    assert result == "契約期間は1年間です。"

    repository.find_by_id.assert_called_once_with(1)
    ai_client.generate_chat.assert_called_once_with(
        doc_text="契約期間は1年間です。", question="契約期間は？"
    )


def test_chat_with_doc_document_not_found():
    repository = MagicMock()
    ai_client = MagicMock()

    repository.find_by_id.return_value = None

    service = DocumentService(repository, ai_client)

    request = ChatRequest(
        document_id=999,
        question="契約期間は？",
    )

    with pytest.raises(DocumentNotFoundError):
        service.chat_with_doc(request)

    ai_client.generate_chat.assert_not_called()


def test_chat_with_doc_content_empty():
    repository = MagicMock()
    ai_client = MagicMock()

    document = Document(
        id=1,
        title="Test Document",
        content=None,
    )

    repository.find_by_id.return_value = document

    service = DocumentService(repository, ai_client)

    request = ChatRequest(
        document_id=1,
        question="内容は？",
    )

    with pytest.raises(DocumentContentEmptyError):
        service.chat_with_doc(request)

    ai_client.generate_chat.assert_not_called()
