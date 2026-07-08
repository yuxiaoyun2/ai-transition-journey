from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    DocumentContentEmptyError,
    DocumentNotFoundError,
    InvalidFileTypeError,
    AIServiceError,
    PDFParseError,
)


async def document_not_found_handler(
    request: Request,
    exc: DocumentNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"error": exc.message},
    )


async def document_content_empty_handler(
    request: Request,
    exc: DocumentContentEmptyError,
):
    return JSONResponse(status_code=400, content={"error": exc.message})


async def invalid_file_type_handler(
    request: Request,
    exc: InvalidFileTypeError,
):
    return JSONResponse(status_code=400, content={"error": exc.message})


async def ai_service_handler(
    request: Request,
    exc: AIServiceError,
):
    return JSONResponse(status_code=503, content={"error": exc.message})


async def pdf_parse_handler(
    request: Request,
    exc: PDFParseError,
):
    return JSONResponse(status_code=500, content={"error": exc.message})
