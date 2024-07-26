from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    #
    time.sleep(4)

    try:
        driver.find_element(
            By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"
        ).click()
    except Exception as e:
        print(f"Scraper{key} cookie Button: {e}")

    time.sleep(4)
    
    flag = True
    while flag:
        time.sleep(4)
        try:
            driver.find_element(By.CSS_SELECTOR, ".button-load-more-circle").click()
        except Exception:
            flag = False

    items = driver.find_elements(By.CSS_SELECTOR, ".search-results-container a[class=\"group\"]")

    data = []

    for item in items:
        link = item.get_attribute("href")
        location = item.find_element(By.CSS_SELECTOR, "span").text.strip()
        for str in locations:
            if str in location:
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".career-result-h").text.strip(),
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
