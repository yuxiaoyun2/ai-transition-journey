from fastapi import UploadFile
from uuid import uuid4

import pypdf
import os
import shutil

from app.services.embedding_service import EmbeddingService
from app.repositories.chroma_repository import ChromaRepository
from app.repositories.document_repository import DocumentRepository
from app.models.document_model import Document
from app.schemas.pdf_schema import UploadResponse

UPLOAD_DIR = "uploads"


class PDFService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        chroma_repository: ChromaRepository,
        document_repository: DocumentRepository,
    ):
        self.embedding_service = embedding_service
        self.chroma_repository = chroma_repository
        self.document_repository = document_repository

    def upload_pdf(
        self,
        title: str,
        file: UploadFile,
    ) -> bool:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        filename = file.filename or "unknown.pdf"
        filepath = os.path.join(UPLOAD_DIR, file.filename)

        self.save_file(
            file=file,
            filepath=filepath,
        )

        file.file.seek(0)

        text = self.pdf_to_text(file)

        if not text.strip():
            raise ValueError("PDFからテキストを抽出できませんでした。")

        document = Document(title=title, filename=filename, filepath=filepath)

        document = self.document_repository.create(document)

        chunks = self.split_text(text)

        embeddings = self.embedding_service.embedding_create(chunks)

        ids = self.get_ids(
            document_id=document.id,
            chunk_count=len(chunks),
        )

        metadatas = self.get_metadatas(
            document_id=document.id,
            title=title,
            filename=file.filename or "unknown.pdf",
            chunk_count=len(chunks),
        )

        chroma = self.chroma_repository.insert(
            ids=ids,
            embeddings=embeddings,
            chunks=chunks,
            metadatas=metadatas,
        )

        return UploadResponse(success=chroma, message="Upload completed.")

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

    def pdf_to_text(
        self,
        file: UploadFile,
    ) -> str:
        reader = pypdf.PdfReader(file.file)

        texts = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                texts.append(page_text)

        return "\n".join(texts)

    def split_text(
        self,
        text: str,
        chunk_size: int = 500,
        overlap: int = 100,
    ) -> list[str]:

        if overlap > chunk_size:
            raise ValueError("overlapはchunk_sizeより小さくしてください。")

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

    def get_metadatas(
        self,
        document_id: str,
        title: str,
        filename: str,
        chunk_count: int,
    ) -> list[dict]:
        return [
            {
                "document_id": document_id,
                "title": title,
                "filename": filename,
                "chunk_index": i,
            }
            for i in range(chunk_count)
        ]
