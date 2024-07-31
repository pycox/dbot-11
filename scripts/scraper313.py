from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    try:
        button = driver.find_element(By.CSS_SELECTOR, "a[data-ui='clear-filters']")
        driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button)
    except:
        print("No filter to clear")
    
    data = []
    
    flag = True
    while flag:
        time.sleep(4)
        try:
            button = driver.find_element(By.CSS_SELECTOR, "button[data-ui='load-more-button']")
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
        except Exception:
            flag = False
    
    items = driver.find_elements(By.CSS_SELECTOR, ".styles--1Px_L ul li")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "div[data-ui='job-location']").text.strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
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
