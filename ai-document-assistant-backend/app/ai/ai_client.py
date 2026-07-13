from app.config import OPENAI_API_KEY, SUMMARY_PROMPT, OPENAI_MODEL, PROMPT
from app.core.logger import logger
from openai import OpenAI, OpenAIError
from app.exceptions.custom_exceptions import AIServiceError


class AIClient:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_summary(self, text: str) -> str:
        try:

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

        except OpenAIError as exc:
            raise AIServiceError() from exc

        answer = response.choices[0].message.content

        return answer

    def generate_chat(self, doc_text: str, question: str) -> str:
        try:
            user_prompt = self.build_chat_prompt(
                document_text=doc_text,
                question=question,
            )
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": PROMPT,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
            )
        except OpenAIError as exc:
            raise AIServiceError() from exc

        answer = response.choices[0].message.content

        return answer

    def build_chat_prompt(
        self,
        document_text: str,
        question: str,
    ) -> str:
        return "Document:\n" f"{document_text}\n\n" "Question:\n" f"{question}"
