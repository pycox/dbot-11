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

    items = []

    doms = driver.find_elements(By.CSS_SELECTOR, "div[data-listing-id='21339'] > div")

    for dom in doms:
        items = items + dom.find_elements(By.CSS_SELECTOR, "div.jet-listing-grid__item")

    data = []

    for item in items:
        link = (
            item.find_element(By.CSS_SELECTOR, "div.make-column-clickable-elementor")
            .get_attribute("data-column-clickable")
            .strip()
        )
        title = item.find_element(By.CSS_SELECTOR, "h4").text.strip()
        location = item.find_elements(
            By.CSS_SELECTOR, "span.jet-listing-dynamic-terms__link"
        )[1].text.strip()
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
