from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []

    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, "div[data-id=\"8bbddac\"] p strong")
        for item in items:
            title = item.text.split(":")[-1].strip()
            data.append(
                [
                    title,
                    com,
                    "United Kingdom",
                    url,
                ]
            )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
