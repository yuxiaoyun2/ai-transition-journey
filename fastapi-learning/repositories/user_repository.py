from database import get_connection


def find_all():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name
            FROM users
            """
        )

        rows = cursor.fetchall()

        return rows


def find_by_id(user_id: int):
    with get_connection() as conn:
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

        return row


def save(name: str):
    with get_connection() as conn:
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

        return user_id


def update(user_id: int, name: str):
    with get_connection() as conn:
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

        return updated


def delete(user_id: int):
    with get_connection() as conn:

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

        return deleted
