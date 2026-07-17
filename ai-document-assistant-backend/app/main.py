from fastapi import FastAPI

from app.database import Base, engine
from app.routers.documents import router as document_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Document Assistant Backend")

app.include_router(document_router)


@app.get("/")
def read_root():
    return {"message": "AI Document Assistant Backend is running"}
