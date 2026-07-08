class DocumentNotFoundError(Exception):
    def __init__(self, message: str = "Document not found"):
        self.message = message
        super().__init__(self.message)


class DocumentContentEmptyError(Exception):
    def __init__(self, message: str = "Document content is empty"):
        self.message = message
        super().__init__(self.message)


class InvalidFileTypeError(Exception):
    def __init__(self, message: str = "Invalid file type"):
        self.message = message
        super().__init__(self.message)


class AIServiceError(Exception):
    def __init__(self, message: str = "AI service is currently unavailable"):
        self.message = message
        super().__init__(self.message)


class PDFParseError(Exception):
    def __init__(self, message: str = "Failed to parse PDF file"):
        self.message = message
        super().__init__(self.message)
