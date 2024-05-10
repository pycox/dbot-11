from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import readUrl, updateDB
import time


def main():
    key = 420
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    driver.find_element(By.CSS_SELECTOR, 'button.acceptAllCookies').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '.modal-content button[aria-label="Close"]').click()
    time.sleep(2)
    
    items = driver.find_elements(By.CSS_SELECTOR, ".section__content .section__entry p span a")
    
    for item in items:
        title, location = item.text.replace(">>", "").strip().split("-")
        link = item.get_attribute("href").strip()
        for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
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


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
