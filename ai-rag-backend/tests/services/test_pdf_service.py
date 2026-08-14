import pytest
from unittest.mock import MagicMock, patch

from app.services.pdf_service import PDFService
from app.models.document_model import Document
from app.exceptions.custom_exceptions import DocumentNotFoundError
from app.core.config import Settings


@patch("app.services.pdf_service.os.remove")
@patch("app.services.pdf_service.os.path.exists")
def test_pdf_service(
    mock_exists,
    mock_remove,
):
    embedding_service = MagicMock()
    chroma_repository = MagicMock()
    document_repository = MagicMock()
    settings = MagicMock(spec=Settings)

    pdf_service = PDFService(
        embedding_service=embedding_service,
        chroma_repository=chroma_repository,
        document_repository=document_repository,
        settings=settings,
    )

    document = Document(
        id=1, title="test title", filename="test.pdf", filepath="/upload/test.pdf"
    )
    document_repository.get_by_id.return_value = document

    mock_exists.return_value = True

    result = pdf_service.delete_document(document_id=1)

    assert result.success is True
    assert result.message == "Document deleted successfully."

    document_repository.get_by_id.assert_called_once_with(document_id=1)

    document_repository.delete.assert_called_once_with(document=document)

    chroma_repository.delete_by_document_id.assert_called_once_with(document_id=1)

    mock_exists.assert_called_once_with("/upload/test.pdf")

    mock_remove.assert_called_once_with("/upload/test.pdf")


@patch("app.services.pdf_service.os.remove")
@patch("app.services.pdf_service.os.path.exists")
def test_pdf_not_found(
    mock_exists,
    mock_remove,
):
    embedding_service = MagicMock()
    chroma_repository = MagicMock()
    document_repository = MagicMock()
    settings = MagicMock(spec=Settings)

    pdf_service = PDFService(
        embedding_service=embedding_service,
        chroma_repository=chroma_repository,
        document_repository=document_repository,
        settings=settings,
    )

    document_repository.get_by_id.return_value = None

    with pytest.raises(DocumentNotFoundError) as exc_info:
        pdf_service.delete_document(document_id=1)

    assert exc_info.value.message == "Document not found"

    document_repository.get_by_id.assert_called_once_with(document_id=1)

    document_repository.delete.assert_not_called()

    chroma_repository.delete_by_document_id.assert_not_called()

    mock_exists.assert_not_called()

    mock_remove.assert_not_called()
