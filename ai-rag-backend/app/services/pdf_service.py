from fastapi import UploadFile
from uuid import uuid4

import pypdf
import os
import shutil

from app.services.embedding_service import EmbeddingService
from app.repositories.chroma_repository import ChromaRepository

UPLOAD_DIR = "uploads"


class PDFService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        repository: ChromaRepository,
    ):
        self.embedding_service = embedding_service
        self.chromadb = repository

    def upload_pdf(
        self,
        title: str,
        file: UploadFile,
    ) -> bool:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        text = self.pdf_to_text(file)

        if not text.strip():
            raise ValueError("PDFからテキストを抽出できませんでした。")

        chunks = self.split_text(text)

        embeddings = self.embedding_service.embedding_create(chunks)

        document_id = str(uuid4())

        ids = self.get_ids(
            document_id=document_id,
            chunk_count=len(chunks),
        )

        metadatas = self.get_metadatas(
            document_id=document_id,
            title=title,
            filename=file.filename or "unknown.pdf",
            chunk_count=len(chunks),
        )

        return self.chromadb.insert(
            ids=ids,
            embeddings=embeddings,
            chunks=chunks,
            metadatas=metadatas,
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
