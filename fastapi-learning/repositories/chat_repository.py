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
