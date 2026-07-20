import os

from app.core.config import get_settings


settings = get_settings()

os.environ["OPENAI_API_KEY"] = settings.openai_api_key
