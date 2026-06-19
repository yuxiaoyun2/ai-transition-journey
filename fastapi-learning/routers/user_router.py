from fastapi import APIRouter, HTTPException

from models.user import UserCreate, UserUpdate
from services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter()


@router.get("/users")
def get_users():
    return get_all_users()


@router.get("/users/{user_id}")
def get_user(user_id: int):
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found",
        )

    return user


@router.post("/users", status_code=201)
def create_new_user(user: UserCreate):
    return create_user(user.name)


@router.put("/users/{user_id}")
def update_existing_user(
    user_id: int,
    user: UserUpdate,
):
    success = update_user(user_id, user.name)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {"id": user_id, "name": user.name}


@router.delete("/users/{user_id}")
def delete_exixting_user(user_id: int):

    success = delete_user(user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "user deleted"}
