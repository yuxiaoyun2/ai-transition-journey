import pytest

from app.exceptions.custom_exceptions import (
    DocumentContentEmptyError,
    DocumentNotFoundError,
)
from app.models.document import Document
from app.schemas.document import ChatRequest


def test_chat_with_doc_success(repository, ai_client, service):
    document = Document(
        id=1,
        title="Test Document",
        content="契約期間は1年間です。",
    )

    repository.find_by_id.return_value = document
    ai_client.generate_chat.return_value = "契約期間は1年間です。"

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


def test_chat_with_doc_document_not_found(repository, ai_client, service):
    repository.find_by_id.return_value = None

    request = ChatRequest(
        document_id=999,
        question="契約期間は？",
    )

    with pytest.raises(DocumentNotFoundError):
        service.chat_with_doc(request)

    ai_client.generate_chat.assert_not_called()


def test_chat_with_doc_content_empty(repository, ai_client, service):
    document = Document(
        id=1,
        title="Test Document",
        content=None,
    )

    repository.find_by_id.return_value = document

    request = ChatRequest(
        document_id=1,
        question="内容は？",
    )

    with pytest.raises(DocumentContentEmptyError):
        service.chat_with_doc(request)

    ai_client.generate_chat.assert_not_called()
