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

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    items = driver.find_elements(By.CSS_SELECTOR, ".Bloom__Tabs__tabsContent___T5H80 .Bloom__modifiers__cf___2jEl0")
    data = []

    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        title = item.find_element(By.CSS_SELECTOR, "h3").text.strip()
        location = item.find_element(By.CSS_SELECTOR, "a p").text.strip()

        for str in locations:
            if str in location:
                data.append(
                    [
                        title,
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
