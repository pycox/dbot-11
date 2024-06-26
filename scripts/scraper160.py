from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main():
    key = 160
    com, url = readUrl(key)
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

    data = []

    # items = driver.find_elements(By.CSS_SELECTOR, "div.job-vacancy")

    # for item in items:
    #     link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
    #     title = item.find_element(
    #         By.CSS_SELECTOR, "div.job-vacancy__title"
    #     ).text.strip()
    #     location = item.find_elements(By.CSS_SELECTOR, "div.job-vacancy__table > div")[
    #         2
    #     ].text.strip()

    #     data.append(
    #         [
    #             title,
    #             com,
    #             location,
    #             link,
    #         ]
    #     )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
