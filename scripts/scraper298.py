from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 298
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    # items = driver.find_elements(By.CSS_SELECTOR, "div.sc-6exb5d-2.ftcjTl")
    # for item in items:
    #     link = item.find_element(By.CSS_SELECTOR, "a.sc-s03za1-0.hcxBWR").get_attribute("href").strip()
    #     location = item.find_element(By.CSS_SELECTOR, "li.custom-css-style-job-location").text.strip()
    #      for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
    #         if (str in location):
    #             data.append(
    #                 [
    #                     item.find_element(By.CSS_SELECTOR, "a.sc-6exb5d-1.iYKKpk").text.strip(),
    #                     com,
    #                     location,
    #                     link,
    #                 ]
    #             )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
