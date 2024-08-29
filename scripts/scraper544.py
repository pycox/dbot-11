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

    time.sleep(3)

    try:
        driver.find_element(By.CSS_SELECTOR, '#hs-eu-confirmation-button').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    regions = ["UK", "US"]

    items = driver.find_elements(By.CSS_SELECTOR, ".hhs-accordion-1.accordion-controls")
    for index, location in enumerate(regions):
        if location in locations:
            try:
                sub_items = items[index].find_elements(By.CSS_SELECTOR, "li a h4")
            except:
                continue
            for sub_item in sub_items:
                data.append(
                    [
                        sub_item.text.strip(),
                        com,
                        location,
                        url,
                    ]
                )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
