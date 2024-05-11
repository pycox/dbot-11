from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 476
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".job-item-content")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a.job-description").get_attribute("href").strip()
        data.append(
            [
                item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                com,
                "London, UK",
                link,
            ]
        )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
