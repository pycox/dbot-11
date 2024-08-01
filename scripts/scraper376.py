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

    data = []
    time.sleep(8)
    
    items = driver.find_elements(By.CSS_SELECTOR, '.whr-items .whr-item')
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, ".whr-title a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, '.whr-location').text.split(":")[-1].strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".whr-title a").text.strip(),
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
