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
    #
    time.sleep(4)

    try:
        driver.find_element(
            By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"
        ).click()
    except Exception as e:
        print(f"Scraper{key} cookie Button: {e}")

    time.sleep(4)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)

    items = driver.find_elements(By.CSS_SELECTOR, "li.BambooHR-ATS-Jobs-Item")

    data = []

    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(
            By.CSS_SELECTOR, "span.BambooHR-ATS-Location"
        ).text.strip()

        for str in locations:
            if str in location:
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
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
