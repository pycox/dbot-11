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

    time.sleep(8)

    data = []

    items = driver.find_elements(By.CSS_SELECTOR, 'li[data-ui="job"]')

    for item in items:
        location = item.find_element(By.CSS_SELECTOR, 'div[data-ui="job-location"]').text.strip()
        for str in locations:
            if (str in location):
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, 'h3[data-ui="job-title"]').text.strip(),
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
