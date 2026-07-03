from app.repositories.document_repository import DocumentRepository
from typing import Optional
from app.models.document import Document
import os
import shutil
from fastapi import UploadFile

UPLOAD_DIR = "uploads"


class DocumentService:
    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    def create_doc(self, title: str, content: str) -> Document:
        doc = Document(title=title, content=content)
        return self.repository.insert(doc)

    def get_all_documnets(self) -> list[Document]:
        return self.repository.find_all()

    def get_doc_by_id(self, document_id: int) -> Optional[Document]:
        return self.repository.find_by_id(document_id)

    def romove_document(self, document_id: int):
        doc = self.repository.find_by_id(document_id)

        if doc is None:
            return False

        self.repository.delete(doc)
        return True

    def save_uploaded_file(self, file: UploadFile) -> str:
        if not UPLOAD_DIR:
            os.makedirs(UPLOAD_DIR)

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file.filename

    def upload_document(self, title: str, file: UploadFile) -> Document:
        filename = self.save_uploaded_file(file)
        doc = Document(
            title=title,
            content=None,
            file_name=filename,
            summary=None,
        )

        return self.repository.insert(doc)
