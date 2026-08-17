from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.models.document_model import Document

client = TestClient(app)


@patch("app.services.pdf_service.os.remove")
@patch("app.services.pdf_service.os.path.exists")
@patch("app.routers.pdf.ChromaRepository")
@patch("app.routers.pdf.get_openai_client")
def test_pdf_delete(
    mock_openai_client,
    mock_chroma_class,
    mock_exists,
    mock_remove,
    test_session_factory,
):
    mock_chroma_instance = mock_chroma_class.return_value

    mock_exists.return_value = True

    setup_db = test_session_factory()

    document = Document(
        title="test document",
        filename="test.pdf",
        filepath="/tmp/test.pdf",
    )
    setup_db.add(document)
    setup_db.commit()
    setup_db.refresh(document)

    document_id = document.id
    filepath = document.filepath

    setup_db.close()

    response = client.delete(f"/pdf/{document_id}")

    assert response.status_code == 200

    assert response.json() == {
        "success": True,
        "message": "Document deleted successfully.",
    }

    verify_db = test_session_factory()

    deleted_document = (
        verify_db.query(Document).filter(Document.id == document_id).first()
    )

    assert deleted_document is None

    verify_db.close()

    mock_chroma_instance.delete_by_document_id.assert_called_once_with(
        document_id=document_id
    )

    mock_exists.assert_any_call(filepath)

    mock_remove.assert_called_once_with(filepath)


@patch("app.services.pdf_service.os.remove")
@patch("app.services.pdf_service.os.path.exists")
@patch("app.routers.pdf.ChromaRepository")
@patch("app.routers.pdf.get_openai_client")
def test_pdf_delete_no_document(
    mock_openai_client,
    mock_chroma_class,
    mock_exists,
    mock_remove,
    test_session_factory,
):
    response = client.delete("/pdf/999")

    assert response.status_code == 404

    assert response.json() == {"error": "Document not found"}

    mock_chroma = mock_chroma_class.return_value

    mock_chroma.delete_by_document_id.assert_not_called()
    # mock_exists.assert_not_called()
    mock_remove.assert_not_called()
