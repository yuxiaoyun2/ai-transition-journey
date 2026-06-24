from database import get_connection


def save_chat_message(user_message: str, ai_answer: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO chat_messages(user_message,ai_answer)
    VALUES(?, ?)
    """,
        (user_message, ai_answer),
    )

    conn.commit()

    chat_id = cursor.lastrowid

    conn.close()

    return chat_id


def find_all_chat_messages():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT id, user_message, ai_answer, created_at
    FROM chat_messages
    ORDER BY id DESC
    """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def find_recent_chat_messages(limit: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT id, user_message, ai_answer, created_at
    FROM chat_messages
    ORDER BY id DESC
    LIMIT ?
    """,
        (limit,),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_all_chat_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    DELETE FROM chat_messages
    """
    )

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted


def save_chat_summary(summary: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO chat_summaries(summary)
    VALUES(?)
    """,
        (summary,),
    )

    conn.commit()

    summary_id = cursor.lastrowid

    conn.close()

    return summary_id


def find_latest_chat_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT id, summary, create_at
    FROM chat_summaries
    ORDER BY id DESC
    LIMIT 1
    """,
    )

    row = cursor.fetchone()

    conn.close()

    return row
