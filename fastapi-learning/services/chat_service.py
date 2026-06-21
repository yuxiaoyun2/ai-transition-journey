from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(message: str) -> str:
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )

    return response.choices[0].message.content
