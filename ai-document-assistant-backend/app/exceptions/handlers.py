from fastapi import Request
from fastapi.responses import JSONResponse
from app.main import app

from app.exceptions.custom_exceptions import (
    DocumentContentEmptyError,
    DocumentNotFoundError,
    InvalidFileTypeError,
    AIServiceError,
    PDFParseError,
)
from app.core.logger import logger


@app.exception_handler(DocumentNotFoundError)
async def document_not_found_handler(
    request: Request,
    exc: DocumentNotFoundError,
):
    return error_response(400, exc.message)


@app.exception_handler(DocumentContentEmptyError)
async def document_content_empty_handler(
    request: Request,
    exc: DocumentContentEmptyError,
):
    logger.warning(f"{request.method} {request.url} : {exc.message}")
    return error_response(400, exc.message)


@app.exception_handler(InvalidFileTypeError)
async def invalid_file_type_handler(
    request: Request,
    exc: InvalidFileTypeError,
):
    logger.warning(f"{request.method} {request.url} : {exc.message}")
    return error_response(400, exc.message)


@app.exception_handler(AIServiceError)
async def ai_service_handler(
    request: Request,
    exc: AIServiceError,
):
    logger.error(f"{request.method} {request.url} : {exc.message}")
    return error_response(503, exc.message)


@app.exception_handler(PDFParseError)
async def pdf_parse_handler(
    request: Request,
    exc: PDFParseError,
):
    logger.error(f"{request.method} {request.url} : {exc.message}")
    return error_response(500, exc.message)


def error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": message})
