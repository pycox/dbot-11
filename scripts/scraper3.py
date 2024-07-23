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
    
    flag = True
    data = []
    
    while flag:
        try:
            time.sleep(4)
            
            items = driver.find_elements(By.CSS_SELECTOR, "article.article--result")
            
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                location  = item.find_element(By.CSS_SELECTOR, 'span.item--location').text.strip()
                
                for str in locations:
                    if str in location:
                        data.append([
                            item.find_element(By.CSS_SELECTOR, "div.article__header__title").text.strip(),
                            com,
                            location,
                            link
                        ])
                        break
                
            nextBtn = driver.find_elements(By.CSS_SELECTOR, 'a.paginationNextLink')

            if len(nextBtn) > 0:
                nextBtn[0].click()
            else:
                flag = False
        except:
            flag = False
            
    updateDB(key, data)
    
    
if __name__ == "__main__":
    main()
    
    
    