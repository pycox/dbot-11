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
        driver.find_element(By.CSS_SELECTOR, 'button#CybotCookiebotDialogBodyButtonDecline').click()
    except:
        print("No Cookie Button")
    time.sleep(4)

    data = []
    
    if "UK" in locations:
    
        items = driver.find_elements(By.CSS_SELECTOR, ".rt-list__items .rt-list__offer-item")
        for item in items:
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, ".rt-list__offer-title").text.strip(),
                    com,
                    "UK",
                    url,
                ]
            )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
