from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL

from repositories.chat_repository import (
    save_chat_message,
    find_all_chat_messages,
    delete_all_chat_history,
    find_recent_chat_messages,
)

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(message: str) -> str:
    messages = build_openai_messages(message)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
    )

    answer = response.choices[0].message.content

    save_chat_message(
        user_message=message,
        ai_answer=answer,
    )

    return answer


def get_chat_history():
    rows = find_all_chat_messages()

    return [
        {
            "id": row[0],
            "user_message": row[1],
            "ai_answer": row[2],
            "created_at": row[3],
        }
        for row in rows
    ]


def get_recent_chat_history(limit: int):
    return find_recent_chat_messages(limit)


def delete_chat_history():
    return delete_all_chat_history()


def build_openai_messages(message: str):
    recent_rows = reversed(get_recent_chat_history(5))

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant",
        }
    ]

    for row in recent_rows:
        messages.append({"role": "user", "content": row[1]})
        messages.append({"role": "assistant", "content": row[2]})

    messages.append({"role": "user", "content": message})

    return messages
