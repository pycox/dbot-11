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
    
    data = []

    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".attrax-vacancy-tile--clifford-chance")
        for item in items:
            location = item.find_element(By.CSS_SELECTOR, ".attrax-vacancy-tile__location-freetext .attrax-vacancy-tile__item-value").text.strip()
            for str in locations:
                if (str in location):
                    link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break
                
        try:
            button = driver.find_element(By.CSS_SELECTOR, 'li a[aria-label="Next pagination page"]')
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
