import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", "10"))

config = Config()