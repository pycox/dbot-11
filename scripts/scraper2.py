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
    
    try:
        driver.find_element(By.CSS_SELECTOR, "button#c-p-bn").click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
        
    time.sleep(4)
    
    items = driver.find_elements(By.CSS_SELECTOR, "div.rt-tr-group")
    
    data = []
    
    if location == "UK":
        locations = ["UK", "United Kingdom"]
    elif location == "US":
        locations = ["US", "United States"]
    else:
        locations = ["US", "UK", "United Kingdom", "United States"]

    
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_elements(By.CSS_SELECTOR, "div.rt-td")[1].text.strip()
        
        for str in locations:
            if (str in location):
                data.append([
                    item.find_elements(By.CSS_SELECTOR, "div.rt-td")[0].text.strip(),
                    com,
                    location,
                    link
                ])
                
                break
        
    updateDB(key, data)


if __name__ == "__main__":
    main()