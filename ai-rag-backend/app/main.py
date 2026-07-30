from app.core.openai_init import init_openai

from fastapi import FastAPI

from app.database import Base, engine
from app.routers.pdf import router as rag_router

Base.metadata.create_all(bind=engine)

init_openai()

app = FastAPI(
    title="AI RAG Backend",
    description="Backend API for an AI RAG",
    version="1.0.0",
)

app.include_router(
    rag_router,
    prefix="/pdf",
    tags=["PDF"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
