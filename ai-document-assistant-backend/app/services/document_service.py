from app.repositories.document_repository import DocumentRepository
from typing import Optional
from app.models.document import Document


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
