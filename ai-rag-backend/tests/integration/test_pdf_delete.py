from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models.document_model import Document

client = TestClient(app)


@patch("app.services.pdf_service.os.remove")
@patch("app.services.pdf_service.os.path.exists")
@patch("app.routers.pdf.ChromaRepository")
@patch("app.routers.pdf.get_openai_client")
def test_pdf_delete(
    mock_openai_client, mock_chroma_class, mock_exists, mock_remove, tmp_path
):

    db_path = tmp_path / "test.db"

    database_url = f"sqlite:///{db_path}"

    test_engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )

    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    mock_chroma_instance = mock_chroma_class.return_value

    mock_exists.return_value = True

    try:
        db = TestSessionLocal()

        document = Document(
            title="test document",
            filename="test.pdf",
            filepath="/tmp/test.pdf",
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        db.close()

        document_id = document.id

        response = client.delete(f"/pdf/{document_id}")

        assert response.status_code == 200

        assert response.json() == {
            "success": True,
            "message": "Document deleted successfully.",
        }

        verify_db = TestSessionLocal()

        deleted_document = (
            verify_db.query(Document).filter(Document.id == document_id).first()
        )

        assert deleted_document is None

        verify_db.close()

        mock_chroma_instance.delete_by_document_id.assert_called_once_with(
            document_id=document_id
        )

        mock_exists.assert_any_call(document.filepath)

        mock_remove.assert_called_once_with(document.filepath)

    finally:
        app.dependency_overrides.pop(
            get_db,
            None,
        )
        test_engine.dispose()


@patch("app.services.pdf_service.os.remove")
@patch("app.services.pdf_service.os.path.exists")
@patch("app.routers.pdf.ChromaRepository")
@patch("app.routers.pdf.get_openai_client")
def test_pdf_delete_no_document(
    mock_openai_client, mock_chroma_class, mock_exists, mock_remove, tmp_path
):
    db_path = tmp_path / "test.db"

    database_url = f"sqlite:///{db_path}"

    test_engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )

    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.delete(f"/pdf/999")

        assert response.status_code == 404

        assert response.json() == {"error": "Document not found"}

        mock_chroma = mock_chroma_class.return_value

        mock_chroma.delete_by_document_id.assert_not_called()
        mock_exists.assert_not_called()
        mock_remove.assert_not_called()

    finally:
        app.dependency_overrides.pop(
            get_db,
            None,
        )
        test_engine.dispose()
