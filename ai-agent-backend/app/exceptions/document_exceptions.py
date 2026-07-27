class DocumentNotFoundError(Exception):
    def __init__(self, message: str = "Document not found."):
        self.message = message
        super().__init__(self.message)
