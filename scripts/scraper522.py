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

    time.sleep(3)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button[data-hook="consent-banner-apply-button"]').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, 'h2[style="text-align:center; font-size:40px;"]')
    try:
        items = items[1:-1]
    except:
        items = []
    for item in items:
        data.append(
            [
                item.text.strip(),
                com,
                "UK",
                url,
            ]
        )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
