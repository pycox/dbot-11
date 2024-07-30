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


    data = []

    items = driver.find_elements(By.CSS_SELECTOR, "ul.b--careers-list-a > li")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, 'span.b--careers-list-a__list-item__link__item-right').text.strip()

        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "span.b--careers-list-a__list-item__link__item-left").text.strip(),
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
