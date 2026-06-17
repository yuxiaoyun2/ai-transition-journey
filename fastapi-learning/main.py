from fastapi import FastAPI

from routers.user_router import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/health")
def health():
    return {"status": "ok"}
