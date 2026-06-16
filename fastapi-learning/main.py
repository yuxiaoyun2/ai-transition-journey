from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users = [{"id": 1, "name": "Tom"}, {"id": 2, "name": "Alice"}]


class UserCreate(BaseModel):
    name: str


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users")
def get_users():
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

    return {"error": "user not found"}


@app.post("/users")
def create_user(user: UserCreate):

    new_user = {"id": len(users) + 1, "name": user.name}

    users.append(new_user)

    return new_user
