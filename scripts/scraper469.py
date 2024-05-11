from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 469
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button.button.cookie-consent__button:nth-child(1)').click()
    except:
        print("No Cookie Button")

    time.sleep(4)

    data = []

    try:
        driver.find_element(By.CSS_SELECTOR, ".cc-job-list__view-more a").click()
        time.sleep(4)
    except Exception:
        print("No more button")

    items = driver.find_elements(By.CSS_SELECTOR, ".job-tile.job-grid-item")
    location = "London, UK"
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        data.append(
            [
                item.find_element(By.CSS_SELECTOR, ".job-tile__title").text.strip(),
                com,
                location,
                link,
            ]
        )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
