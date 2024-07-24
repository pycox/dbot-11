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
    
    time.sleep(8)
    
    try:
        driver.find_element(By.CSS_SELECTOR, 'button.cky-btn-accept').click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
        
    time.sleep(4)
    
    items = driver.find_elements(By.CSS_SELECTOR, 'ul.advert-list > li')
    
    data = []
    
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, 'span.location').text.strip()
        title = item.find_element(By.CSS_SELECTOR, 'span.role').text.strip()
        
        for str in locations:
            if (str in location):
                data.append([title, com, location, link])
                
                break
        
    updateDB(key, data)


if __name__ == "__main__":
    main()
    