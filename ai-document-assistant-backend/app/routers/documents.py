from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    MessageResponse,
    ChatRequest,
    ChatResponse,
)
from app.services.document_service import DocumentService
from app.repositories.document_repository import DocumentRepository
from app.ai.ai_client import AIClient
from sqlalchemy.orm import Session
from app.database import get_db


router = APIRouter(prefix="/documents", tags=["documents"])


def get_document_service(db: Session = Depends(get_db)) -> DocumentService:
    repository = DocumentRepository(db)
    ai_client = AIClient()
    return DocumentService(repository, ai_client)


@router.post("", status_code=201, response_model=DocumentResponse)
def create_doc(
    request: DocumentCreate,
    service: DocumentService = Depends(get_document_service),
):
    return service.create_doc(
        title=request.title,
        content=request.content,
    )


@router.get("", response_model=list[DocumentResponse])
def list_docs(
    service: DocumentService = Depends(
        get_document_service,
    )
):
    return service.get_all_documents()


@router.get("/{document_id}", response_model=DocumentResponse)
def get_doc(
    document_id: int,
    service: DocumentService = Depends(get_document_service),
):
    doc = service.get_doc_by_id(document_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc


@router.delete("/{document_id}", response_model=MessageResponse)
def delete_doc(
    document_id,
    service: DocumentService = Depends(get_document_service),
):
    deleted = service.remove_document(document_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "deleted success"}


@router.post("/upload", response_model=DocumentResponse)
def upload_doc(
    title: str,
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    return service.upload_document(title=title, file=file)


@router.post("/chat", response_model=ChatResponse)
def chat_with_doc(
    request: ChatRequest,
    service: DocumentService = Depends(get_document_service),
):
    try:
        answer = service.chat_with_doc(request)
        return {"answer": answer}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
