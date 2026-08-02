from fastapi import APIRouter, File, UploadFile, Depends

from app.services.pdf_service import PDFService
from app.services.retrieval_service import RetrievalService
from app.repositories.chroma_repository import ChromaRepository
from app.services.embedding_service import EmbeddingService
from app.repositories.document_repository import DocumentRepository
from app.schemas.pdf_schema import UploadResponse
from app.schemas.search_schema import SearchResponse, SearchRequest
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


def get_retrieval_service() -> RetrievalService:
    embedding_service = EmbeddingService()
    chroma_repository = ChromaRepository()

    return PDFService(
        embedding_service,
        chroma_repository,
    )


@router.post("/upload", response_model=UploadResponse)
def upload_pdf(
    title: str,
    file: UploadFile = File(...),
    service: PDFService = Depends(get_pdf_service),
):
    return service.upload_pdf(
        title,
        file,
    )


@router.post("", response_model=SearchResponse)
def search_documents(
    request: SearchRequest,
    service: RetrievalService = Depends(get_retrieval_service),
):
    return service.search(
        question=request.question,
        top_k=request.top_k,
    )
