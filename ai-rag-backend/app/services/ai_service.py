from openai import OpenAI, OpenAIError
from app.core.config import get_settings
from app.exceptions.custom_exceptions import AIServiceError
from app.core.logger import logger


class AIService:

    def __init__(self, client: OpenAI):
        self.client = client

    def generate_chat(
        self,
        prompt: str,
    ) -> str:
        try:
            settings = get_settings()
            response = self.client.chat.completions.create(
                model=settings.openai_chat_model,
                messages=[{"role": "user", "content": prompt}],
            )

        except OpenAIError as exc:
            logger.exception("OpenAI chat request failed")
            raise AIServiceError() from exc

        content = response.choices[0].message.content

        return content or ""
