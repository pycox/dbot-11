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
    
    items = driver.find_elements(By.CSS_SELECTOR, ".current-openings-list .current-openings-item")
    for item in items:
        location = item.find_element(By.CSS_SELECTOR, "label.current-opening-location-item").text.strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "span.current-opening-title").text.strip(),
                        com,
                        location,
                        url,
                    ]
                )
                break

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
