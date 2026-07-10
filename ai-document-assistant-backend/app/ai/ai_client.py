from app.config import OPENAI_API_KEY, SUMMARY_PROMPT, OPENAI_MODEL, PROMPT
from app.core.logger import logger
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

        logger.info("Generate AI summary")

        answer = response.choices[0].message.content

        return answer

    def generate_chat(self, doc_text: str, question: str) -> str:
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": PROMPT,
                },
                {
                    "role": "user",
                    "content": f"""
                    Document:
                    {doc_text}
                    
                    Question:
                    {question}
                    """,
                },
            ],
        )

        answer = response.choices[0].message.content

        return answer
