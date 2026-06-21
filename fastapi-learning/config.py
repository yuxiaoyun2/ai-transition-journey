from dotenv import load_dotenv

import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "app.db")
APP_NAME = os.getenv("APP_NAME", "FastAPI")
