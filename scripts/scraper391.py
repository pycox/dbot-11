from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 391
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

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, "div.job-listing .job-summary")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, ".job-summary-heading a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".job-summary-location").text.strip()
            for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break

        try:
            driver.find_element(By.CSS_SELECTOR, 'li.page-next').click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
