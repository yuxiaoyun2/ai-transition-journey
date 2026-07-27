from app.repositories.document_repository import DocumentRepository
from app.exceptions.document_exceptions import DocumentNotFoundError


class DocumentService:
    def __init__(self):
        self.repository = DocumentRepository()

    def search_document(
        self,
        keyword: str,
    ) -> str:
        result = self.repository.search(keyword=keyword)

        if result is None:
            raise DocumentNotFoundError()

        return result
