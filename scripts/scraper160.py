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
            "button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
        ).click()
    except Exception as e:
        print(f"Scraper{key} cookiee button: {e}")

    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, "#job-listings li"))
    time.sleep(4)

    data = []

    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, "#job-listings li a")

        for item in items:
            link = item.get_attribute("href").strip()
            title = item.text.strip()
            title = driver.execute_script("return arguments[0].innerText;", item)
            data.append(
                [
                    title.strip(),
                    com,
                    "UK",
                    link,
                ]
            )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
