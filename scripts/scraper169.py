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
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(2)

    data = []

    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, "#openings h3")

        for item in items:
            data.append(
                [
                    item.text.strip(),
                    com,
                    "UK",
                    url,
                ]
            )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
