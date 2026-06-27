from database import get_connection


def save_chat_message(user_message: str, ai_answer: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO chat_messages(user_message,ai_answer)
            VALUES(?, ?)
            """,
            (
                user_message,
                ai_answer,
            ),
        )

        conn.commit()

        chat_id = cursor.lastrowid

        return chat_id


def find_all_chat_messages():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, user_message, ai_answer, created_at
            FROM chat_messages
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        return rows


def find_recent_chat_messages(limit: int):
    with get_connection() as conn:
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

        return rows


def delete_all_chat_history():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM chat_messages
            """
        )

        conn.commit()

        deleted = cursor.rowcount

        return deleted


def save_chat_summary(summary: str):
    with get_connection() as conn:

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

        return summary_id


def find_latest_chat_summary():
    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, summary, created_at
            FROM chat_summaries
            ORDER BY id DESC
            LIMIT 1
            """,
        )

        row = cursor.fetchone()

        return row


def count_chat_messages():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM chat_messages
            """
        )

        count = cursor.fetchone()[0]

        return count


def count_chat_summaries():
    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM chat_summaries
            """
        )

        count = cursor.fetchone()[0]

        return count


def find_latest_chat_time():
    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT Max(created_at)
            FROM chat_messages
            """
        )

        latest_time = cursor.fetchone()[0]

        return latest_time
