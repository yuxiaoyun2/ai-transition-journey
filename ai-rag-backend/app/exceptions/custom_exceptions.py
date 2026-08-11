class AppError(Exception):

    default_message = "Application error"

    def __init__(
        self,
        message: str | None = None,
    ):
        self.message = message or self.default_message

        super().__init__(self.message)


class DocumentNotFoundError(AppError):
    default_message = "Document not found"


class InvalidPDFError(AppError):
    default_message = "Invalid PDF file"


class RetrievalError(AppError):
    default_message = "Retrieval error"


class AIServiceError(AppError):
    default_message = "AI service is currently unavailable"


class TopkCheckError(AppError):
    default_message = "top_kは1以上である必要があります。"


class MetadataNotFoundError(AppError):
    default_message = "Metadataが存在しません。"


class ChunkCreateError(AppError):
    default_message = "Chunkを生成できませんでした。"


class OverlapSettingError(AppError):
    default_message = "overlapはchunk_sizeより小さくしてください。"
