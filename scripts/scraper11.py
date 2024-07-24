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
    driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='Location_Country']").click()
    time.sleep(2)
    if all(loc in locations for loc in ["UK", "US"]):
        driver.find_element(By.XPATH, "//label[contains(text(), 'United Kingdom')]").click()
        time.sleep(4)
        driver.find_element(By.XPATH, "//label[contains(text(), 'United States')]").click()
    elif "UK" in locations:
        driver.find_element(By.XPATH, "//label[contains(text(), 'United Kingdom')]").click()
    else:
        driver.find_element(By.XPATH, "//label[contains(text(), 'United States')]").click()
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
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                                
                data.append([
                    item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                    com,
                    item.find_element(By.CSS_SELECTOR, "dd").text.strip(),
                    link
                ])
                    
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
    