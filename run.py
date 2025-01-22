from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib
import os
from utils import filterUrls

from dotenv import load_dotenv

load_dotenv()

num_threads = int(os.getenv("SPEED") or 10)


def scraping(id, name, url):
    try:
        print(f"======== {int(id / 600 * 10000) / 100.0}% ========")

        scrapper = importlib.import_module(f"scripts.scraper{id}")

        scrapper.main(id, name, url)
    except Exception as e:
        print(f"{name}: {e}")


def run():
    scrapers = filterUrls()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(scraping, *attrs) for attrs in scrapers]

        for future in as_completed(futures):
            if future.exception() is not None:
                print(f"An error occurred: {future.exception()}")


if __name__ == "__main__":
    run()
