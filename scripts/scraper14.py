from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time


def main(key, com, url):
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    time.sleep(10)
    
    try:
        driver.find_element(By.CSS_SELECTOR, "button#ccc-recommended-settings").click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
        
    time.sleep(2)
        
    try:
        driver.find_element(By.CSS_SELECTOR, "span#cn-notice-buttons").click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
    
    # data = []
    
    # items = driver.find_elements(By.CSS_SELECTOR, 'li.search-result ')
    
    # data = []
    
    # for item in items:
    #     link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
    #     location = item.find_element(By.CSS_SELECTOR, "div.posting-subtitle").text.strip().split("●")[0]
            
    #     if location.split(',')[-1].strip() in ["USA", "UK"]:
    #         data.append([
    #         item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
    #         com,
    #         location,
    #         link
    #     ])
            
    # updateDB(key, data)
    
    
if __name__ == "__main__":
    main()
    
    
    
    