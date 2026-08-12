from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    DocumentNotFoundError,
    InvalidPDFError,
    AIServiceError,
    RetrievalError,
    TopkCheckError,
    MetadataNotFoundError,
    ChunkCreateError,
    OverlapSettingError,
)
from app.core.logger import logger


def register_exception_handlers(
    app: FastAPI,
) -> None:

    @app.exception_handler(DocumentNotFoundError)
    async def document_not_found_handler(
        request: Request,
        exc: DocumentNotFoundError,
    ):
        return error_response(404, exc.message)

    @app.exception_handler(InvalidPDFError)
    async def invalid_pdf_handler(
        request: Request,
        exc: InvalidPDFError,
    ):
        logger.warning(
            "Invalid PDF: path=%s message=%s",
            request.url.path,
            exc.message,
        )
        return error_response(
            400,
            exc.message,
        )

    @app.exception_handler(AIServiceError)
    async def ai_service_handler(
        request: Request,
        exc: AIServiceError,
    ):
        return error_response(
            503,
            exc.message,
        )

    @app.exception_handler(RetrievalError)
    async def retrieval_handler(
        request: Request,
        exc: RetrievalError,
    ):
        return error_response(
            500,
            exc.message,
        )

    @app.exception_handler(TopkCheckError)
    async def top_k_check_handler(
        request: Request,
        exc: TopkCheckError,
    ):
        return error_response(
            400,
            exc.message,
        )

    @app.exception_handler(MetadataNotFoundError)
    async def metadata_not_found_handler(
        request: Request,
        exc: MetadataNotFoundError,
    ):
        return error_response(
            404,
            exc.message,
        )

    @app.exception_handler(ChunkCreateError)
    async def chunk_create_handler(
        request: Request,
        exc: ChunkCreateError,
    ):
        return error_response(
            500,
            exc.message,
        )

    @app.exception_handler(OverlapSettingError)
    async def overlap_setting_handler(
        request: Request,
        exc: OverlapSettingError,
    ):
        return error_response(
            400,
            exc.message,
        )

    def error_response(status_code: int, message: str):
        return JSONResponse(
            status_code=status_code,
            content={"error": message},
        )
