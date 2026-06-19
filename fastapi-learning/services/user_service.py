from database import get_connection


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT id, name 
    FROM users
    """
    )

    rows = cursor.fetchall()

    conn.close()

    return [{"id": row[0], "name": row[1]} for row in rows]


def get_user_by_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None
    return {
        "id": row[0],
        "name": row[1],
    }


def create_user(name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users(name)
        VALUES(?)
        """,
        (name,),
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return {"id": user_id, "name": name}


def update_user(user_id: int, name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET name = ?
        WHERE id = ?
        """,
        (name, user_id),
    )

    conn.commit()
    updated = cursor.rowcount

    conn.close()

    return updated > 0


def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        (user_id,),
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    return deleted > 0
