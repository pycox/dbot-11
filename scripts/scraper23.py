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
        driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler').click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
      
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1000);")
            
    time.sleep(6)
    
    items = driver.find_elements(By.CSS_SELECTOR, 'ul li .vacancies-list-item')
    data = []
    
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute("href").strip()
        location = item.find_elements(By.CSS_SELECTOR, 'div.ds-grid__col')[2].text.strip()
        title = item.find_element(By.CSS_SELECTOR, 'a').text.strip()
        for str in locations:
            if (str in location):
                data.append([title, com, location, link])
                
                break
        
    updateDB(key, data)


if __name__ == "__main__":
    main()
    