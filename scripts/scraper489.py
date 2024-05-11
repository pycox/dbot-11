from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 489
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    
    try:
        driver.find_element(By.CSS_SELECTOR, 'Button#ccc-recommended-settings').click()
    except:
        print("No Cookie Button")

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, "div#block-iab-content li a")
    for item in items:
        link = item.get_attribute("href").strip()
        data.append(
            [
                item.text.strip(),
                com,
                "UK",
                link,
            ]
        )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
