from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 394
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
    
    items = driver.find_elements(By.CSS_SELECTOR, ".w-dyn-list div[role='listitem']")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = "London"
        data.append(
            [
                item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                com,
                location,
                link,
            ]
        )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
