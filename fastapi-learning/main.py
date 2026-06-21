from fastapi import FastAPI
from config import APP_NAME
from database import init_db
from routers.user_router import router as user_router
from routers.chat_router import router as chat_router

app = FastAPI(title=APP_NAME)

init_db()

app.include_router(user_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/health")
def health():
    return {"status": "ok"}
