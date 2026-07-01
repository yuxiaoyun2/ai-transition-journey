from fastapi import FastAPI

from app.database import Base, engine
from app.models.document import Document

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Document Assistant Backend")


@app.get("/")
def read_root():
    return {"message": "AI Document Assistant Backend is running"}
