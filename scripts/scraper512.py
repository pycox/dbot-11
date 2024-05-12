from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 512
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []

    items = driver.find_elements(By.CSS_SELECTOR, ".job-list li")
    for item in items:
        link = f"{url}?jobId={item.get_attribute('id')}"
        location = item.find_element(By.CSS_SELECTOR, ".location-info").text.strip()
        for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".job-title").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )
                break


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
