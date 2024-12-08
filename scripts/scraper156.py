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

    data = []

    time.sleep(4)

    time.sleep(4)
    items = driver.find_elements(By.CSS_SELECTOR, ".open-position-listing.w-dyn-item")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, '.open-position-item-wrapper:nth-child(3)').text.strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".open-position-title").text.strip(),
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
