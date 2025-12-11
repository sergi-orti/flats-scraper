# run_once.py
from scrapy.crawler import CrawlerProcess

from scraper import IdealistaSpider
from config import *
from mongo_repository import get_mongo_client, get_collection

def run():
    client = get_mongo_client(
        MONGO_HOST, MONGO_PORT,
        MONGO_USER, MONGO_PASSWORD,
        MONGO_AUTH_DB
    )
    collection = get_collection(client, MONGO_DB, MONGO_COLLECTION)

    settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 1,
        "LOG_LEVEL": "INFO",
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
    }

    process = CrawlerProcess(settings)
    process.crawl(
        IdealistaSpider,
        start_url=IDEALISTA_URL,
        mongo_collection=collection,
        telegram_token=TELEGRAM_TOKEN,
        telegram_chat_id=TELEGRAM_CHAT_ID
    )
    process.start()

if __name__ == "__main__":
    run()
