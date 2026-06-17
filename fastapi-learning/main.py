from fastapi import FastAPI

from database import init_db
from routers.user_router import router

app = FastAPI()

init_db()

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/health")
def health():
    return {"status": "ok"}
