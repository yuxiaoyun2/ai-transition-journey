from fastapi import FastAPI
from app.database import Base, engine
from app.routers.pdf import router as rag_router
from app.routers.search import router as search_router
from app.routers.chat import router as chat_router
from app.exceptions.handlers import register_exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI RAG Backend",
    description="Backend API for an AI RAG",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(
    rag_router,
    prefix="/pdf",
    tags=["PDF"],
)

app.include_router(
    search_router,
    prefix="/search",
    tags=["Search"],
)

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["chat"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
