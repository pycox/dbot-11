from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main():
    key = 453
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)


    data = []

    # items = driver.find_elements(By.CSS_SELECTOR, ".css-1fquksq.e9up25i0")
    # for item in items:
    #     link = url
    #     location = item.find_element(By.CSS_SELECTOR, '.css-11lck9.e9up25i5').text.strip()
    #     for str in ['LONDON', 'NEW YORK', 'SAN FRANCISCO', 'UNITED STATES', 'UNITED KINGDOM', 'UK', 'USA', 'US']:
    #         if (str in location):
    #             data.append(
    #                 [
    #                     item.find_element(By.CSS_SELECTOR, ".css-1wh1a53.e9up25i6").text.strip(),
    #                     com,
    #                     location,
    #                     link,
    #                 ]
    #             )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
