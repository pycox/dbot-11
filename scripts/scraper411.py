from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 411
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    if url.endswith("/"):
        url = url[:-1]
    driver.get(url)

    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".open-roles .open-role")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, ".open-role-location").text.strip()
        for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".open-role-title").text.strip(),
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
