from openai import OpenAI, OpenAIError
from app.core.config import Settings
from app.exceptions.custom_exceptions import AIServiceError
from app.core.logger import logger


class AIService:

    def __init__(self, client: OpenAI, settings: Settings):
        self.client = client
        self.settings = settings

    def generate_chat(
        self,
        prompt: str,
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.settings.openai_chat_model,
                messages=[{"role": "user", "content": prompt}],
            )

        except OpenAIError as exc:
            logger.exception("OpenAI chat request failed")
            raise AIServiceError() from exc

        content = response.choices[0].message.content

        return content or ""
