from app.repositories.document_repository import DocumentRepository
from app.models.document import Document
from app.ai.ai_client import AIClient
from app.schemas.document import ChatRequest

import os
import shutil
from typing import Optional

from fastapi import UploadFile
import pypdf


UPLOAD_DIR = "uploads"


class DocumentService:
    def __init__(self, repository: DocumentRepository, ai_client: AIClient):
        self.repository = repository
        self.ai_client = ai_client

    def create_doc(self, title: str, content: str) -> Document:
        doc = Document(title=title, content=content)
        return self.repository.insert(doc)

    def get_all_documents(self, limit: int, offset: int) -> list[Document]:
        return self.repository.find_all(limit, offset)

    def get_doc_by_id(self, document_id: int) -> Optional[Document]:
        return self.repository.find_by_id(document_id)

    def remove_document(self, document_id: int):
        doc = self.repository.find_by_id(document_id)

        if doc is None:
            return False

        self.repository.delete(doc)
        return True

    def save_uploaded_file(self, file: UploadFile, file_path: str) -> str:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file.filename

    def upload_document(self, title: str, file: UploadFile) -> Document:
        if not UPLOAD_DIR:
            os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        filename = self.save_uploaded_file(file, file_path)

        text = self.pdf_to_text(file_path)

        summary = self.ai_client.generate_summary(text)

        doc = Document(
            title=title,
            content=text,
            file_name=filename,
            summary=summary,
        )

        return self.repository.insert(doc)

    def pdf_to_text(self, path) -> str:
        reader = pypdf.PdfReader(path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    def chat_with_doc(self, request: ChatRequest):
        doc = self.get_doc_by_id(request.document_id)

        if doc is None:
            raise ValueError("no exists docment")

        if not doc.content:
            raise ValueError("Document content is empty")

        return self.ai_client.generate_chat(doc.content, request.question)

    def get_docs_by_keyword(self, keyword: str) -> list[Document]:
        return self.repository.find_by_keyword(keyword)
