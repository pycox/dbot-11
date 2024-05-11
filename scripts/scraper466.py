from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 466
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    # flag = True
    # while flag:
    #     time.sleep(4)
    #     try:
    #         driver.find_element(By.CSS_SELECTOR, "div.d-flex.mt-4.ng-star-inserted > button").click()
    #     except Exception:
    #         flag = False
    
    # items = driver.find_elements(By.CSS_SELECTOR, "li.careers-listings-item")
    # for item in items:
    #     link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
    #     location = item.find_element(By.CSS_SELECTOR, ".careers-listings-item--location").text.strip()
    #     for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
    #         if (str in location):
    #             data.append(
    #                 [
    #                     item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
    #                     com,
    #                     location,
    #                     link,
    #                 ]
    #             )
    #             break


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
