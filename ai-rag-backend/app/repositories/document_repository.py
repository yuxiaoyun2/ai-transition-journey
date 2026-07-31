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
