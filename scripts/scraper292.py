from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main():
    key = 292
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    data = []
    flag = True

    while flag:
        time.sleep(4)
        try:
            driver.find_element(By.CSS_SELECTOR, "div.d-flex.mt-4.ng-star-inserted > button").click()
        except Exception:
            flag = False

    items = driver.find_elements(By.CSS_SELECTOR, ".row.job-item.ng-star-inserted")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, ".btn.btn-outline-primary").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, '.text-muted.font-weight-bold').text.strip()

        for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h5").text.strip(),
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
