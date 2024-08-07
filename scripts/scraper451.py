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
        driver.find_element(By.CSS_SELECTOR, 'button#hs-eu-decline-button').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(4)

    data = []
    
    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, "a.career__listing")
        for item in items:
            link = item.get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, ".career__listing--title").text.strip(),
                    com,
                    "UK",
                    link,
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
