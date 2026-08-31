from fastapi import UploadFile

import pypdf
from pypdf.errors import PdfReadError
import os
import shutil
from uuid import uuid4
from pathlib import Path

from app.services.embedding_service import EmbeddingService
from app.repositories.chroma_repository import ChromaRepository
from app.repositories.document_repository import DocumentRepository
from app.models.document_model import Document
from app.schemas.pdf_schema import UploadResponse, DeleteDocumentResponse
from app.schemas.search_schema import ChunkMetadata
from app.exceptions.custom_exceptions import ChunkCreateError, OverlapSettingError
from app.exceptions.custom_exceptions import InvalidPDFError, DocumentNotFoundError
from app.core.logger import logger
from app.core.config import Settings


class PDFService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        chroma_repository: ChromaRepository,
        document_repository: DocumentRepository,
        settings: Settings,
    ):
        self.embedding_service = embedding_service
        self.chroma_repository = chroma_repository
        self.document_repository = document_repository
        self.settings = settings

    def upload_pdf(
        self,
        title: str,
        file: UploadFile,
    ) -> UploadResponse:
        document = None
        original_filename = file.filename or "unknown.pdf"

        suffix = Path(original_filename).suffix

        stored_filename = f"{uuid4()}{suffix}"

        filepath = os.path.join(
            self.settings.upload_dir,
            stored_filename,
        )

        try:
            if not file.filename.lower().endswith(".pdf"):
                raise InvalidPDFError("PDFファイルのみアップロードできます。")

            if not os.path.exists(self.settings.upload_dir):
                os.makedirs(self.settings.upload_dir)

            self.save_file(
                file=file,
                filepath=filepath,
            )

            file.file.seek(0)

            pages = self.pdf_to_pages(file)

            obj = Document(title=title, filename=original_filename, filepath=filepath)
            document = self.document_repository.create(obj)

            chunks = []
            metadatas = []

            for page in pages:
                page_chunks = self.split_text(page["text"])

                for chunk_index, chunk in enumerate(page_chunks):
                    chunks.append(chunk)

                    metadata = ChunkMetadata(
                        document_id=document.id,
                        title=document.title,
                        filename=document.filename,
                        page_number=page["page_number"],
                        chunk_index=chunk_index,
                    )

                    metadatas.append(metadata.model_dump())

            if not chunks:
                raise ChunkCreateError()

            embeddings = self.embedding_service.embeddings_create(chunks)

            ids = self.get_ids(
                document_id=document.id,
                chunk_count=len(chunks),
            )

            success = self.chroma_repository.insert(
                ids=ids,
                embeddings=embeddings,
                chunks=chunks,
                metadatas=metadatas,
            )

        except Exception:
            self._rollback_upload(document=document, filepath=filepath)
            raise

        return UploadResponse(success=success, message="Upload completed.")

    def _rollback_upload(
        self,
        document: Document | None,
        filepath: str,
    ) -> None:
        try:
            if document is not None:
                self.chroma_repository.delete_by_document_id(document_id=document.id)
        except Exception:
            logger.exception("Rollback failed: chroma cleanup")

        try:
            if document is not None:
                self.document_repository.delete(document=document)
        except Exception:
            logger.exception("Rollback failed: database cleanup")

        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            logger.exception("Rollback failed: file cleanup")

    def save_file(
        self,
        file: UploadFile,
        filepath: str,
    ) -> None:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

    def pdf_to_pages(
        self,
        file: UploadFile,
    ) -> list[dict]:

        try:
            reader = pypdf.PdfReader(file.file)
        except PdfReadError as exc:
            raise InvalidPDFError("PDFファイルを読み込めませんでした。") from exc

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            text = page.extract_text() or ""

            if text.strip():
                pages.append(
                    {
                        "page_number": page_number,
                        "text": text,
                    }
                )

        return pages

    def split_text(
        self,
        text: str,
    ) -> list[str]:
        chunk_size = self.settings.chunk_size
        overlap = self.settings.chunk_overlap

        if overlap >= chunk_size:
            raise OverlapSettingError()

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += chunk_size - overlap

        return chunks

    def get_ids(
        self,
        document_id: str,
        chunk_count: int,
    ) -> list[str]:
        return [f"{document_id}_{i}" for i in range(chunk_count)]

    def delete_document(self, document_id: int) -> DeleteDocumentResponse:
        try:
            document = self.document_repository.get_by_id(document_id=document_id)

            if document is None:
                raise DocumentNotFoundError()

            self.chroma_repository.delete_by_document_id(document_id=document_id)

            if os.path.exists(document.filepath):
                os.remove(document.filepath)

            self.document_repository.delete(document=document)

        except DocumentNotFoundError:
            raise

        except Exception:
            logger.exception(
                "Failed to delete document: document_id=%s",
                document_id,
            )
            raise

        logger.info(
            "Document deleted successfully: document_id=%s",
            document_id,
        )

        return DeleteDocumentResponse(
            success=True, message="Document deleted successfully."
        )
