from sqlalchemy.orm import Session
from app.models.document import Document
from typing import Optional


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert(self, obj: Document) -> Document:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def find_all(self) -> list[Document]:
        return self.db.query(Document).all()

    def find_by_id(self, _id: int) -> Optional[Document]:
        return self.db.get(Document, _id)

    def delete(self, obj: Document) -> None:
        self.db.delete(obj)
        self.db.commit()
