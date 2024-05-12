from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main():
    key = 504
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    
    try:
        driver.find_element(By.CSS_SELECTOR, 'button#cookie-accept').click()
        time.sleep(4)
    except:
        print("No Cookiee") 
        
    try:
        driver.find_element(By.CSS_SELECTOR, 'a[title="Find experienced jobs"]').click()
        time.sleep(4)
    except:
        print("No Page") 
           
    data = []

    total_jobs = driver.find_element(By.CSS_SELECTOR, 'div#content b:nth-child(2)').text.strip()
    total_jobs = int(total_jobs)
    current_jobs = 25

    while current_jobs < total_jobs:
        items = driver.find_elements(By.CSS_SELECTOR, "tr.data-row")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, 'span.jobLocation').text.strip()
            title = item.find_element(By.CSS_SELECTOR, "a").text.strip()
            for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US', 'GB']:
                if (str in location):
                    data.append(
                        [
                            title,
                            com,
                            location,
                            link,
                        ]
                    )
                    break
        
        current_jobs += 25
        if current_jobs < total_jobs:
            driver.get(f"{url}ey/search/?q=&sortColumn=referencedate&sortDirection=desc&startrow={current_jobs}")
            time.sleep(4)


    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
