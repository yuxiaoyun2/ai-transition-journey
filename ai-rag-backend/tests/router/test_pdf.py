import pytest
from fastapi.testclient import TestClient
from starlette.datastructures import UploadFile
from unittest.mock import MagicMock

from app.main import app
from app.schemas.pdf_schema import UploadResponse, DeleteDocumentResponse
from app.routers.pdf import get_pdf_service
from app.exceptions.custom_exceptions import InvalidPDFError, DocumentNotFoundError

client = TestClient(app)


def test_pdf_upload():
    mock_service = MagicMock()

    mock_service.upload_pdf.return_value = UploadResponse(
        success=True,
        message="uploaded",
    )

    def override_pdf_service():
        return mock_service

    app.dependency_overrides[get_pdf_service] = override_pdf_service

    try:
        response = client.post(
            "/pdf/upload",
            data={
                "title": "test title",
            },
            files={
                "file": (
                    "test.pdf",
                    b"dummy pdf content",
                    "application/pdf",
                )
            },
        )

        assert response.status_code == 200

        assert response.json() == {
            "success": True,
            "message": "uploaded",
        }

        mock_service.upload_pdf.assert_called_once()

        _, kwargs = mock_service.upload_pdf.call_args

        assert kwargs["title"] == "test title"
        assert isinstance(
            kwargs["file"],
            UploadFile,
        )
        assert kwargs["file"].filename == "test.pdf"

    finally:
        app.dependency_overrides.pop(
            get_pdf_service,
            None,
        )


def test_invalid_pdf_error():
    mock_service = MagicMock()

    mock_service.upload_pdf.side_effect = InvalidPDFError()

    def override_pdf_service():
        return mock_service

    app.dependency_overrides[get_pdf_service] = override_pdf_service

    try:
        response = client.post(
            "/pdf/upload",
            data={
                "title": "test title",
            },
            files={
                "file": (
                    "test.pdf",
                    b"dummy pdf content",
                    "application/pdf",
                )
            },
        )

        assert response.status_code == 400

        assert response.json() == {"error": "Invalid PDF file"}

        mock_service.upload_pdf.assert_called_once()

    finally:
        app.dependency_overrides.pop(
            get_pdf_service,
            None,
        )


def test_pdf_delete():
    mock_service = MagicMock()

    mock_service.delete_document.return_value = DeleteDocumentResponse(
        success=True,
        message="Document deleted successfully.",
    )

    def override_pdf_service():
        return mock_service

    app.dependency_overrides[get_pdf_service] = override_pdf_service

    try:
        response = client.delete("/pdf/1")

        assert response.status_code == 200

        assert response.json() == {
            "success": True,
            "message": "Document deleted successfully.",
        }

        mock_service.delete_document.assert_called_once_with(document_id=1)

    finally:
        app.dependency_overrides.pop(
            get_pdf_service,
            None,
        )


def test_pdf_delete_error():
    mock_service = MagicMock()

    mock_service.delete_document.side_effect = DocumentNotFoundError()

    def override_pdf_service():
        return mock_service

    app.dependency_overrides[get_pdf_service] = override_pdf_service

    try:
        response = client.delete(
            "/pdf/1",
        )

        assert response.status_code == 404

        assert response.json() == {"error": "Document not found"}
        mock_service.delete_document.assert_called_once_with(document_id=1)

    finally:
        app.dependency_overrides.pop(
            get_pdf_service,
            None,
        )
