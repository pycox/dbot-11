from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 513
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="I\'m fine with this"]').click()
    except:
        print("No Cookie Button")
        
    try:
        driver.find_elements(By.CSS_SELECTOR, 'ul#nav-full li')[-1].click()
        time.sleep(6)
    except:
        print("No Page")
    
    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".results-item.vacancy")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, ".vacancy__title a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".vacancy__region").text.strip()
            for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, ".vacancy__title").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break

        try:
            driver.find_element(By.CSS_SELECTOR, 'a.next').click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
