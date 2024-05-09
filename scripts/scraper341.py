from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 341
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".content-item-type-post")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        title_location = item.find_element(By.CSS_SELECTOR, ".content-item-heading-text.heading-text").text.strip().split()
        title, location = " ".join(title_location[:-2]), title_location[-1]
        if location == "Kendal":
            location = f"{location}, UK"
        elif any(substring in location for substring in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']):
            pass
        else:
            continue
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
