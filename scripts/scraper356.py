from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 356
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    for slug, location in [("london", "London, United Kingdom"), ("new-york", "New York, United States")]:
        items = driver.find_elements(By.CSS_SELECTOR, f'div[mb-careers-location="{slug}"] a')
        for item in items:
            link = item.get_attribute("href").strip()
            data.append(
                [
                    item.text.strip(),
                    com,
                    location,
                    link,
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
