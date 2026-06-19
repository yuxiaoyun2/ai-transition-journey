from database import get_connection


def find_all():
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

    return rows


def find_by_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT id , name
    FROM users
    WHERE id = ?
    """,
        (user_id,),
    )

    row = cursor.fetchone()

    conn.close()

    return row


def save(name: str):
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

    return user_id


def update(user_id, name: str):
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

    return updated


def delete(user_id: int):

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

    return deleted
