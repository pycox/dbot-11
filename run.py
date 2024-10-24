from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib
from utils import filterUrls, getBotSpeed, saveData

num_threads = getBotSpeed()


def scraping(id, name, url, location):
    try:
        scrapper = importlib.import_module(f"scripts.scraper{id}")
        scrapper.main(id, name, url, location)
    except Exception as e:
        print(f"{name}: {e}")


def run():
    scrapers = filterUrls()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(scraping, *attrs) for attrs in scrapers]

        for future in as_completed(futures):
            if future.exception() is not None:
                print(f"An error occurred: {future.exception()}")

        saveData()


if __name__ == "__main__":
    run()
