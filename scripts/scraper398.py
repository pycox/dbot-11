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
    
    regions = []

    if "UK" in locations:
        regions.append(("UK", "gb"))

    if "US" in locations:
        regions.append("US", "us")
        
    data = []

    for location, location_code in regions:
        driver.get(f"{url}&country={location_code}")
        time.sleep(4)
        items = driver.find_elements(By.CSS_SELECTOR, ".p-view-jobsearchresults .p-panel.p-p-b-md a[data-tag=\"displayJobTitle\"]")
        for item in items:
            link = item.get_attribute("href").strip()
            data.append(
                [
                    item.text.strip(),
                    com,
                    location,
                    link,
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
