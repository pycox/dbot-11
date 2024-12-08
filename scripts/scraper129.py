from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time


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

    items = driver.find_elements(By.CSS_SELECTOR, ".content-panel-container .content-panel.contact-block")

    data = []
    regions = []

    if "US" in locations:
        regions.extend(("New York", "Los Angeles"))
    if "UK" in locations:
        regions.append("London")

    for item in items:
        location = item.find_element(By.CSS_SELECTOR, '.contact-header-pnl p').text.strip()
        if location not in regions:
            continue
        sub_items = item.find_elements(By.CSS_SELECTOR, ".job-listings-block a")
        for sub_item in sub_items:
            data.append(
                [
                    sub_item.text.strip(),
                    com,
                    location,
                    sub_item.get_attribute("href").strip(),
                ]
            )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
