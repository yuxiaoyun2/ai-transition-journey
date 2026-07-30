from fastapi import APIRouter, File, UploadFile, Depends

from app.services.pdf_service import PDFService
from app.repositories.chroma_repository import ChromaRepository
from app.services.embedding_service import EmbeddingService

router = APIRouter()


def get_pdf_service() -> PDFService:
    embeddingservice = EmbeddingService()
    repository = ChromaRepository()
    return PDFService(
        embeddingservice,
        repository,
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
