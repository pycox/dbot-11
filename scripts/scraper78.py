from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time
import math


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    total = int(
        driver.find_element(
            By.CSS_SELECTOR, ".paginationLabel b:last-child"
        ).text.strip()
    )

    data = []

    for i in range(0, math.floor(total / 25)):
        if i != 0:
            driver.get(
                f"https://jobs.bentley.com/search?q=&sortColumn=referencedate&sortDirection=desc&searchby=location&d=10000&startrow={i * 25}"
            )

        time.sleep(4)

        items = driver.find_elements(By.CSS_SELECTOR, "tr.data-row")

        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, "td.colLocation").text.strip()
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "td.colTitle").text.strip(),
                            com,
                            str,
                            link,
                        ]
                    )
                    break

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
