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

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".accordians-container .accordion .accordian-content-container")
    for item in items:
        title = item.find_element(By.CSS_SELECTOR, "h2").text.strip().split("-")
        title = title[0]
        if len(title) == 1:
            location = "UK"
        else:
            location = title[1]
            if location != "USA":
                location = "UK"
        
        link = f"{url}#{item.get_attribute('id')}"
        if location in locations:
            data.append(
                [
                    com,
                    location,
                    link,
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
