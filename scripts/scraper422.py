from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, '.c-btn.js-cookie-banner-accept.mr-2').click()
    except:
        print("No Cookie Button")

    time.sleep(4)
    data = []
    
    if "UK" in locations:
        button = driver.find_element(By.CSS_SELECTOR, ".selectric-js-vacancy-locations")
        driver.execute_script("arguments[0].click();", button)
        button = driver.find_element(By.CSS_SELECTOR, ".selectric-js-vacancy-locations li[data-index=\"2\"]")
        driver.execute_script("arguments[0].click();", button)
        button = driver.find_element(By.CSS_SELECTOR, ".c-filter__submit.js-vacancies-filter-submit")
        driver.execute_script("arguments[0].click();", button)

        time.sleep(4)

    
        items = driver.find_elements(By.CSS_SELECTOR, ".vacancy")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                    com,
                    "UK",
                    link,
                ]
            )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
