from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from twisted.internet.task import LoopingCall

from scraper import IdealistaSpider
from mongo_repository import get_mongo_client, get_collection
from config import *

SCRAPING_INTERVAL = 300  # 5 min

client = get_mongo_client(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD, MONGO_AUTH_DB)
collection = get_collection(client, MONGO_DB, MONGO_COLLECTION)
settings = {
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "ROBOTSTXT_OBEY": False,
    "DOWNLOAD_DELAY": 1,
    "LOG_LEVEL": "INFO",
    "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
    "TWISTED_REACTOR": "twisted.internet.selectreactor.SelectReactor",
}
runner = CrawlerRunner(settings)


def run_spider():
    print("Ejecutando spider...")
    return runner.crawl(
        IdealistaSpider,
        start_url=IDEALISTA_URL,
        mongo_collection=collection,
        telegram_token=TELEGRAM_TOKEN,
        telegram_chat_id=TELEGRAM_CHAT_ID
    ).addBoth(lambda _: print("Spider finalizado."))


@defer.inlineCallbacks
def start():
    yield run_spider()
    lc = LoopingCall(run_spider)
    lc.start(SCRAPING_INTERVAL)


if __name__ == "__main__":
    start()
    reactor.run()
