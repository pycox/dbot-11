from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 353
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, ".search-container"))
    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".job-tile-lists .job")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, "ul li:nth-child(1)").text.strip()
            for str in [
                'London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US'
            ]:
                if (str in location):
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
            next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next page"]')
            if "true" == next_button.get_attribute("aria-disabled"):
                flag = False
            else:
                next_button.click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
