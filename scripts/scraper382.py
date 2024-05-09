from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 382
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    # items = driver.find_elements(By.CSS_SELECTOR, "li.list-vacancies__item")
    # for item in items:
    #     link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
    #     location = "London, UK"
    #     data.append(
    #         [
    #             item.find_element(By.CSS_SELECTOR, ".list-vacancies__title").text.strip(),
    #             com,
    #             location,
    #             link,
    #         ]
    #     )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
