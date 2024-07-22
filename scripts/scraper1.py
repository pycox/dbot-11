from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, location):
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    time.sleep(4)
    
    items = driver.find_elements(By.CSS_SELECTOR, "div.sc-uzptka-1")
    
    data = []
    
    if location == "UK":
        locations = ["United Kingdom"]
    elif location == "US":
        locations = ["United States"]
    else:
        locations = ["United Kingdom", "United States"]
        
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "span.custom-css-style-job-location-country").text.strip()
        
        if location.split(',')[-1].strip() in locations:
            data.append([
                item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                com,
                location,
                link
            ])
        
    updateDB(key, data)


if __name__ == "__main__":
    main()