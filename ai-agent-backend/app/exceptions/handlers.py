from app.main import app
from app.exceptions.task_exceptions import AIServiceError

from fastapi import Request
from fastapi.responses import JSONResponse


@app.exception_handler(AIServiceError)
async def ai_service_handler(request: Request, exc: AIServiceError):
    return JSONResponse(status_code=503, content={"error": exc.message})
