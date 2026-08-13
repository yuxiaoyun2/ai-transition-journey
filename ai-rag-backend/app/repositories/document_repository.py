from app.models.document_model import Document
from sqlalchemy.orm import Session


class DocumentRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(self, obj: Document) -> Document:
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)

            return obj

        except Exception:
            self.db.rollback()
            raise

    def get_by_id(
        self,
        document_id: int,
    ) -> Document | None:
        return self.db.query(Document).filter(Document.id == document_id).first()

    def delete(
        self,
        document: Document,
    ) -> None:
        self.db.delete(document)
        self.db.commit()
