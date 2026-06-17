from fastapi import APIRouter

from models.user import UserCreate
from services.user_service import get_all_users, get_user_by_id, create_user

router = APIRouter()


@router.get("/users")
def get_users():
    return get_all_users()


@router.get("/users/{user_id}")
def get_user(user_id: int):
    user = get_user_by_id(user_id)

    if user:
        return user
    return {"error": "user not found"}


@router.post("/users")
def create_new_user(user: UserCreate):
    return create_user(user.name)
