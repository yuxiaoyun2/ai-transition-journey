import pytest
from unittest.mock import MagicMock, patch
from io import BytesIO
from fastapi import UploadFile

from app.services.pdf_service import PDFService
from app.models.document_model import Document
from app.exceptions.custom_exceptions import DocumentNotFoundError, AIServiceError
from app.core.config import Settings


@patch("app.services.pdf_service.os.remove")
@patch("app.services.pdf_service.os.path.exists")
@patch("app.services.pdf_service.PDFService.save_file")
def test_pdf_upload_error(
    mock_save_file,
    mock_exists,
    mock_remove,
):
    embedding_service = MagicMock()
    chroma_repository = MagicMock()
    document_repository = MagicMock()
    settings = MagicMock(spec=Settings)
    settings.upload_dir = "/upload"
    settings.chunk_size = 500
    settings.chunk_overlap = 100

    pdf_service = PDFService(
        embedding_service=embedding_service,
        chroma_repository=chroma_repository,
        document_repository=document_repository,
        settings=settings,
    )

    document = Document(
        id=1,
        title="test title",
        filename="test.pdf",
        filepath="/upload/test.pdf",
    )
    document_repository.create.return_value = document

    mock_exists.return_value = True

    embedding_service.embeddings_create.side_effect = AIServiceError()

    pdf_service.pdf_to_pages = MagicMock(
        return_value=[
            {
                "page_number": 1,
                "text": "test pdf content",
            }
        ]
    )

    upload_file = UploadFile(
        filename="test.pdf",
        file=BytesIO(b"dummy pdf content"),
    )

    with pytest.raises(AIServiceError) as exc_info:
        pdf_service.upload_pdf(title="test", file=upload_file)

    assert exc_info.value.message == "AI service is currently unavailable"

    chroma_repository.delete_by_document_id.assert_called_once_with(document_id=1)

    document_repository.delete.assert_called_once_with(document=document)

    mock_remove.assert_called_once_with("/upload/test.pdf")

    chroma_repository.insert.assert_not_called()


@patch("app.services.pdf_service.os.remove")
@patch("app.services.pdf_service.os.path.exists")
def test_pdf_delete(
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
