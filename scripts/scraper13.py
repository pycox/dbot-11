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
    
    time.sleep(5)
    
    try:
        driver.find_element(By.CSS_SELECTOR, "button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
    except Exception as e:
        print(f'Scraper{key} cookiee button: {e}')
    
    flag = True
    data = []
    
    
    flag = True
    while flag:
        time.sleep(4)
        try:
            driver.find_element(By.CSS_SELECTOR, "div.RecentJobPosts_loadMore__ieWQ5 > button").click()
        except Exception:
            flag = False
    
        items = driver.find_elements(By.CSS_SELECTOR, ".RecentJobPosts_jobs__Y9kYZ a")
        for item in items:
            
            link = item.get_attribute('href')
            location = item.find_elements(By.CSS_SELECTOR, '.RecentJobPosts_tags__z5SPl p')[-1].text.strip()
            for str in locations:
                if str in location:
                    data.append([
                        item.find_element(By.CSS_SELECTOR, "p.heading-4").text.strip(),
                        com,
                        location,
                        link
                    ])
                    break
        
    updateDB(key, data)
    
    
if __name__ == "__main__":
    main()
    
    
    
    