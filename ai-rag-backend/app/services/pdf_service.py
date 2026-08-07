from fastapi import UploadFile

import pypdf
import os
import shutil

from app.services.embedding_service import EmbeddingService
from app.repositories.chroma_repository import ChromaRepository
from app.repositories.document_repository import DocumentRepository
from app.models.document_model import Document
from app.schemas.pdf_schema import UploadResponse
from app.schemas.search_schema import ChunkMetadata

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
    ) -> UploadResponse:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        filename = file.filename or "unknown.pdf"
        filepath = os.path.join(UPLOAD_DIR, filename)

        self.save_file(
            file=file,
            filepath=filepath,
        )

        file.file.seek(0)

        pages = self.pdf_to_pages(file)

        document = Document(title=title, filename=filename, filepath=filepath)

        document = self.document_repository.create(document)

        chunks = []
        metadatas = []

        for page in pages:
            page_chunks = self.split_text(page["text"])

            for chunk_index, chunk in enumerate(page_chunks):
                print(f"===== Chunk {chunk_index} =====")
                print(chunk)
                chunks.append(chunk)

                metadata = ChunkMetadata(
                    document_id=document.id,
                    title=title,
                    filename=filename,
                    page_number=page["page_number"],
                    chunk_index=chunk_index,
                )

                metadatas.append(metadata.model_dump())

        if not chunks:
            raise ValueError("Chunkを生成できませんでした。")

        embeddings = self.embedding_service.embeddings_create(chunks)

        ids = self.get_ids(
            document_id=document.id,
            chunk_count=len(chunks),
        )

        print("pages count:", len(pages))
        print("chunks count:", len(chunks))
        print("ids:", ids)

        success = self.chroma_repository.insert(
            ids=ids,
            embeddings=embeddings,
            chunks=chunks,
            metadatas=metadatas,
        )

        return UploadResponse(success=success, message="Upload completed.")

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
        reader = pypdf.PdfReader(file.file)

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
        chunk_size: int = 500,
        overlap: int = 100,
    ) -> list[str]:

        if overlap >= chunk_size:
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
