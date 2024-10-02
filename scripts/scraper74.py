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

    items = driver.find_elements(By.CSS_SELECTOR, "li.whr-item")

    for item in items:
        link_tag = item.find_element(By.TAG_NAME, "a")
        link = link_tag.get_attribute("href") if link_tag else ""

        location_tag = item.find_element(By.CSS_SELECTOR, "li.whr-location")
        location = location_tag.text.strip() if location_tag else ""

        title_tag = item.find_element(By.TAG_NAME, "h3")
        title = title_tag.text.strip() if title_tag else ""
        data.append(
            [
                title,
                com,
                location,
                link,
            ]
        )
        

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
