from fastapi.testclient import TestClient
from starlette.datastructures import UploadFile
from unittest.mock import MagicMock

from app.main import app
from app.schemas.pdf_schema import UploadResponse
from app.routers.pdf import get_pdf_service
from app.exceptions.custom_exceptions import InvalidPDFError

client = TestClient(app)


def test_pdf_router():
    mock_service = MagicMock()

    mock_service.upload_pdf.return_value = UploadResponse(
        success=True, message="uploaded"
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
        app.dependency_overrides.pop(get_pdf_service, None)


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
        app.dependency_overrides.pop(get_pdf_service, None)
