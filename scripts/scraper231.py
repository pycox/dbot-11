from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    try:
        driver.find_element(By.CSS_SELECTOR, 'button[mode="primary"]').click()
    except:
        print("No Cookie Button")
    time.sleep(4)

    data = []

    items = driver.find_elements(By.CSS_SELECTOR, "#tab-annunci .col-12.col-md-6")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, ".vacancy__title a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "span[title='Location']").text.strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".vacancy__title a").text.strip(),
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
