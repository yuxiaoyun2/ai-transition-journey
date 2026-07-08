from fastapi import FastAPI

from app.database import Base, engine
from app.routers.documents import router as document_router

from app.exceptions.custom_exceptions import (
    DocumentContentEmptyError,
    DocumentNotFoundError,
)

from app.exceptions.handlers import (
    document_content_empty_handler,
    document_not_found_handler,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Document Assistant Backend")

app.include_router(document_router)


@app.get("/")
def read_root():
    return {"message": "AI Document Assistant Backend is running"}


app.add_exception_handler(
    DocumentNotFoundError,
    document_not_found_handler,
)

app.add_exception_handler(DocumentContentEmptyError, document_content_empty_handler)
