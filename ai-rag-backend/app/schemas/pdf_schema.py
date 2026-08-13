from pydantic import BaseModel


class UploadResponse(BaseModel):
    success: bool
    message: str


class DeleteDocumentResponse(BaseModel):
    success: bool
    message: str
