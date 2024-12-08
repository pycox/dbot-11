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

    time.sleep(4)

    data = []
    
    if "UK" in locations:

        tabs = driver.find_elements(By.CSS_SELECTOR, "ul.tabs-nav.r-tabs-nav li")
        for tab in tabs:
            tab.click()
            time.sleep(2)
        
            items = driver.find_elements(By.CSS_SELECTOR, ".jobs__tab.r-tabs-panel.r-tabs-state-active > div.job.js-job")
            for item in items:
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".job__title").text.strip(),
                        com,
                        "UK",
                        url,
                    ]
                )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
