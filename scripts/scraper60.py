from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='distanceLocation']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//label[contains(text(), 'London')]").click()
    time.sleep(4)
    driver.find_element(By.XPATH, "//label[contains(text(), 'New York')]").click()
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='viewAllJobsButton']").click()
    time.sleep(4)
    
    flag = True
    data = []
    
    while flag:
        try:
            time.sleep(4)
            
            items = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
            
            for item in items:
                location = item.find_element(By.CSS_SELECTOR, "dd").text.strip()
                for str in locations:
                    if (str in location):
                        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                                        
                        data.append([
                            item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                            com,
                            location,
                            link
                        ])
                        break
                                
            if len(driver.find_elements(By.CSS_SELECTOR, "button[data-uxi-element-id='next']")) > 0: 
                driver.find_element(By.CSS_SELECTOR, "button[data-uxi-element-id='next']").click()
            else: 
                flag = False
                break
            
        except Exception as e:
            flag = False
            
    updateDB(key, data)


if __name__ == "__main__":
    main()
    