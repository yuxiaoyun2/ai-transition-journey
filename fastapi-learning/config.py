from dotenv import load_dotenv

import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "app.db")
APP_NAME = os.getenv("APP_NAME", "FastAPI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
CHAT_HISTORY_LIMIT = os.getenv("CHAT_HISTORY_LIMIT", "5")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant")
CHAT_SUMMARY_PROMPT = os.getenv(
    "CHAT_SUMMARY_PROMPT", "Please summarize the following conversation briefly."
)
