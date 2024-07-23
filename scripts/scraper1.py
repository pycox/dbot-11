from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    time.sleep(4)
    
    items = driver.find_elements(By.CSS_SELECTOR, "div.sc-uzptka-1")
    
    data = []
    
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "span.custom-css-style-job-location-country").text.strip()
        if location in locations:
            print(location)
            data.append([
                item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                com,
                location,
                link
            ])
        
    updateDB(key, data)


if __name__ == "__main__":
    main()