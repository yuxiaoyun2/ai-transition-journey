import os

from app.core.config import get_settings


def init_openai():

    settings = get_settings()

    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
