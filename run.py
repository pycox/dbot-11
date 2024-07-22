from threading import Thread
import importlib
from utils import updateDB, filterUrls, getBotSpeed

num_threads = getBotSpeed()

scraper_modules = [f"scripts.scraper{id}" for id in filterUrls()]


def scraping(id, name, url, location):
    
    try:
        scrapper = importlib.import_module(f"scripts.scraper{id}")
        scrapper.main(id, name, url, location)
    except Exception as e:
        print(f"{name}: {e}")


def run():
    scrapers = filterUrls()
    total_scrapers = len(scrapers)
    for i in range(0, total_scrapers, num_threads):
        threads = []

        for attrs in scrapers[i : i + num_threads]:
            thread = Thread(target=scraping, args=(attrs))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        updateDB()


if __name__ == "__main__":
    run()
