from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 426
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler').click()
    except:
        print("No Cookie Button")

    time.sleep(4)

    data = []
    
    # items = driver.find_elements(By.CSS_SELECTOR, "div#container-ada44bb3bb ul li")
    # print(items)
    # for item in items:
    #     print(item)
    #     link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
    #     location = item.find_element(By.CSS_SELECTOR, ".careers-listings-item--location").text.strip()
    #     print(location)
    #     for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
    #         if (str in location):
    #             data.append(
    #                 [
    #                     item.find_element(By.CSS_SELECTOR, "a").text.strip(),
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
