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

    try:
        driver.find_element(
            By.CSS_SELECTOR,
            "div.cookie-consent__actions > button",
        ).click()
    except Exception as e:
        print(f"Scraper{key} cookiee button: {e}")

    time.sleep(4)

    items = driver.find_elements(By.CSS_SELECTOR, 'li[data-qa="searchResultItem"]')

    data = []

    for item in items:
        location = item.find_element(By.CSS_SELECTOR, "li:nth-child(1) > div.job-list-item__job-info-value-container > div.job-list-item__job-info-value").text.strip()
        for str in locations:
            if (str in location):
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                title = item.find_element(By.CSS_SELECTOR, "span.job-tile__title").text.strip()
                data.append(
                    [
                        title,
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
