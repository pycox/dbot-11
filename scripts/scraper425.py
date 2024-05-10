from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import readUrl, updateDB
import time


def main():
    key = 425
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    # flag = True
    # while flag:
    #     items = driver.find_elements(By.CSS_SELECTOR, ".list.jobListPanel tbody tr")
    #     for item in items:
    #         link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
    #         title = item.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
    #         location = item.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()
    #         for str in ['Chicago', 'London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
    #             if (str in location):
    #                 data.append(
    #                     [
    #                         title,
    #                         com,
    #                         location,
    #                         link,
    #                     ]
    #                 )
    #                 break

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
