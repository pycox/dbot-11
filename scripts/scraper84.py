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
            "#hs-eu-confirmation-button",
        ).click()
    except Exception as e:
        print(f"Scraper{key} cookie Button: {e}")

    time.sleep(4)

    data = []

    items = driver.find_elements(By.CSS_SELECTOR, ".detail-content > h3")
    for item in items:
        title = item.text.strip()

        # Extract the link from the anchor tag within the h3 element, if it exists
        link = item.find_element(By.XPATH, ".//a").get_attribute("href").strip()

        # Find the following sibling p element for location
        location_element = item.find_element(By.XPATH, "following-sibling::p")
        location = location_element.text.strip()
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
