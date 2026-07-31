from fastapi import APIRouter, File, UploadFile, Depends

from app.services.pdf_service import PDFService
from app.repositories.chroma_repository import ChromaRepository
from app.services.embedding_service import EmbeddingService
from app.repositories.document_repository import DocumentRepository
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


def get_pdf_service(db: Session = Depends(get_db)) -> PDFService:
    embedding_service = EmbeddingService()
    chroma_repository = ChromaRepository()
    document_repository = DocumentRepository(db)

    return PDFService(
        embedding_service,
        chroma_repository,
        document_repository,
    )


@router.post("/upload")
def upload_pdf(
    title: str,
    file: UploadFile = File(...),
    service: PDFService = Depends(get_pdf_service),
):
    return service.upload_pdf(
        title,
        file,
    )
