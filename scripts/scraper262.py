from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main():
    key = 262
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    items = driver.find_elements(By.CSS_SELECTOR, "div.latest-job")

    data = []

    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        fullname = item.find_element(By.CSS_SELECTOR, 'a').text.strip()
        fullname = fullname.split(",")
        location = fullname[-1].strip()

        data.append(
            [
                fullname[0].strip(),
                com,
                location,
                link,
            ]
        )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
