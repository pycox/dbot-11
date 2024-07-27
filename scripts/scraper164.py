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

    try:
        driver.find_element(By.CSS_SELECTOR, "button#truste-consent-button").click()
    except Exception as e:
        print(f"Scraper{key} cookiee button: {e}")

    flag = True

    while flag:
        try:
            button = driver.find_element(By.CSS_SELECTOR, "a[aria-label=\"Load More about jobs\"]")
            driver.execute_script("arguments[0].scrollIntoView();", button)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(4)
        except:
            flag = False
            break

    data = []

    items = driver.find_elements(By.CSS_SELECTOR, "a.filter-box")

    for item in items:
        link = item.get_attribute("href").strip()
        location = item.find_element(
            By.XPATH,
            ".//span[contains(text(), 'Location')]/following-sibling::div",
        ).text.strip()
        for str in locations:
            if (str in location):

                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "div.table-title").text.strip(),
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
