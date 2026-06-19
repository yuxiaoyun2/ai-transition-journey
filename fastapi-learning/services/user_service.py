from repositories.user_repository import (
    find_all,
    find_by_id,
    save,
    update,
    delete,
)


def get_all_users():
    rows = find_all()

    return [{"id": row[0], "name": row[1]} for row in rows]


def get_user_by_id(user_id: int):
    row = find_by_id(user_id)

    if not row:
        return None
    return {
        "id": row[0],
        "name": row[1],
    }


def create_user(name: str):
    user_id = save(name)

    return {"id": user_id, "name": name}


def update_user(user_id: int, name: str):
    updated = update(user_id, name)

    return updated > 0


def delete_user(user_id: int):
    deleted = delete(user_id)

    return deleted > 0
