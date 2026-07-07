from sqlalchemy.orm import Session
from app.models.document import Document
from typing import Optional
from sqlalchemy import or_


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Document

    def insert(self, obj: Document) -> Document:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def find_all(self) -> list[Document]:
        return self.db.query(self.model).all()

    def find_by_id(self, _id: int) -> Optional[Document]:
        return self.db.get(Document, _id)

    def delete(self, obj: Document) -> None:
        self.db.delete(obj)
        self.db.commit()

    def find_by_keyword(self, keyword: str, limit: int = None) -> list[Document]:
        if not keyword or not keyword.strip():
            return self.find_all()

        query = self.db.query(self.model).filter(
            or_(
                self.model.title.contains(keyword),
                self.model.content.contains(keyword),
            )
        )
        if limit is not None:
            query = query.limit(limit)

        return query.all()
