from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 386
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button#truste-consent-required').click()
    except:
        print("No Cookie Button")

    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, ".filters-bottom"))
    
    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        time.sleep(4)
        try:
            driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Load More about jobs"]').click()
        except Exception:
            flag = False
    
    items = driver.find_elements(By.CSS_SELECTOR, "a.table-tr")
    for item in items:
        link = item.get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "div:nth-child(3)").text.strip()
        for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".table-title div").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )
                break


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
