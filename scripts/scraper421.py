from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import readUrl, updateDB
import time


def main():
    key = 421
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    # items = driver.find_elements(By.CSS_SELECTOR, "a")
    
    # for item in items:
    #     title, location = item.text.replace(">>", "").strip().split("-")
    #     link = item.get_attribute("href").strip()
    #     for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
    #         if (str in location):
    #             data.append(
    #                 [
    #                     title,
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
