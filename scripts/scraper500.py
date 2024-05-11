from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import readUrl, updateDB
import time


def main():
    key = 500
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []

    # items = driver.find_elements(By.CSS_SELECTOR, "._container_j2da7_1")
    # for item in items:
    #     link = item.get_attribute("href").strip()
    #     location = item.find_element(By.CSS_SELECTOR, "p").text.split("•")[1].strip()
    #     for str in ['Bournemouth', 'London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
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
