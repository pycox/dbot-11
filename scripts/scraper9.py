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
    
    try:
        driver.find_element(By.CSS_SELECTOR, 'button[data-dojo-attach-point="btnAcceptCookie"]').click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
        
    time.sleep(4)
    
    items = driver.find_elements(By.CSS_SELECTOR, 'li.search-result ')
    
    data = []
    
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "div.posting-subtitle").text.strip().split("●")[0]
            
        for str in locations:
            if str in location:
                if location.split(',')[-1].strip() in ["USA", "UK"]:
                    data.append([
                    item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                    com,
                    location,
                    link
                ])
                break
                
    updateDB(key, data)


if __name__ == "__main__":
    main()
    