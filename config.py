# config.py
from dotenv import load_dotenv
import os

load_dotenv()


IDEALISTA_URL = os.getenv("IDEALISTA_URL")

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_AUTH_DB = os.getenv("MONGO_AUTH_DB")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SCRAPING_INTERVAL = os.getenv("SCRAPING_INTERVAL")
