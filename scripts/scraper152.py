from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    dom = driver.find_element(By.CSS_SELECTOR, ".ashby-job-posting-brief-list")

    items = dom.find_elements(By.CSS_SELECTOR, "a")

    data = []

    for item in items:
        link = item.get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "p").text.split("•")[1].strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
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
