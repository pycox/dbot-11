from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
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
        items = driver.find_elements(By.CSS_SELECTOR, ".jet-listing-grid__item")
        for item in items:
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                    com,
                    "UK",
                    item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip(),
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
