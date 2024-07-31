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

    time.sleep(2)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button#ccc-recommended-settings').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)

    data = []
    
    if "UK" in locations:
        flag = True
        while flag:
            time.sleep(4)
            try:
                driver.find_element(By.CSS_SELECTOR, "button#tile-more-results").click()
            except Exception:
                flag = False
    
        items = driver.find_elements(By.CSS_SELECTOR, ".job-tile-cell")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                    com,
                    "United Kingdom",
                    link,
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
