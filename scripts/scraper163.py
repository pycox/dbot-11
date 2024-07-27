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

    try:
        driver.find_element(
            By.CSS_SELECTOR,
            "#onetrust-accept-btn-handler",
        ).click()
    except Exception as e:
        print(f"Scraper{key} cookiee button: {e}")

    time.sleep(2)

    data = []

    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, ".row-full-width-inner div[data-content-type=\"text\"]")


        for item in items:
            try:
                if not item.find_elements(By.CSS_SELECTOR, "strong"):
                    continue
                title = item.find_elements(By.CSS_SELECTOR, "p")[1].text.strip()
                if not title:
                    continue
                title = title.split("\n")[0].split(":")[1].strip()
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            except:
                continue

            data.append(
                [
                    title,
                    com,
                    "UK",
                    link,
                ]
            )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
