from fastapi import FastAPI

from app.routers.agent_router import router as agent_router

import os

from app.core.config import get_settings

settings = get_settings()

os.environ["OPENAI_API_KEY"] = settings.openai_api_key

app = FastAPI(
    title="AI Agent Backend",
    description="Backend API for an AI task management agent",
    version="1.0.0",
)

app.include_router(agent_router)


@app.get("/health")
async def health_check():
    return {"task": "ok"}
