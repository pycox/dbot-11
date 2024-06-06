from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 535
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".cards__card.card")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        data.append(
            [
                item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                com,
                "United Kingdom",
                link,
            ]
        )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
