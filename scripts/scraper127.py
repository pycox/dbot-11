from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
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

    time.sleep(3)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, "div.l-content__body li a")
    for item in items:
        data.append(
            [
                driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "strong u")).strip(),
                com,
                "US",
                item.get_attribute("href").strip(),
            ]
        )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
