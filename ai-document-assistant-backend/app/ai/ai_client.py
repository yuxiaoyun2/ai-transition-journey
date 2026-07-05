from app.config import OPENAI_API_KEY, SUMMARY_PROMPT, OPENAI_MODEL
from openai import OpenAI


class AIClient:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_summary(self, text: str) -> str:
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SUMMARY_PROMPT,
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
        )

        answer = response.choices[0].message.content

        return answer
