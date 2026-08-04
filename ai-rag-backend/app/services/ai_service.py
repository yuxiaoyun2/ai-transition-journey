from openai import OpenAI, OpenAIError
from app.core.config import get_settings


class AIService:

    def __init__(self, client: OpenAI):
        self.client = client

    def generate_chat(
        self,
        prompt: str,
    ) -> str:
        settings = get_settings()
        response = self.client.chat.completions.create(
            model=settings.openai_chat_model,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content

        return content or ""
