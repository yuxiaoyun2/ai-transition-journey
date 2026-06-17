users = [{"id": 1, "name": "Tom"}, {"id": 2, "name": "Alice"}]


def get_all_users():
    return users


def get_user_by_id(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def create_user(name: str):
    new_user = {"id": len(users) + 1, "name": name}

    users.append(new_user)

    return new_user
