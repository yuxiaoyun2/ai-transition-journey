import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUMMARY_PROMPT = os.getenv("SUMMARY_PROMPT", "以下の文章を要約してください。")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
