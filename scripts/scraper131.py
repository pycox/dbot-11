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

    items = driver.find_elements(By.CSS_SELECTOR, "#openings li  h2 a")
    for item in items:
        data.append(
            [
                item.text.strip(),
                com,
                "UK",
                item.get_attribute("href"),
            ]
        )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
