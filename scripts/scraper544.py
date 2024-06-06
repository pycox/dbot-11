from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 544
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".job-card.job-card-template")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, ".job-card-content .job-tag"))
        for str in ['LONDON', 'NEW YORK', 'SAN FRANCISCO', 'UNITED STATES', 'UNITED KINGDOM']:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".job-title").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )
                break


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
