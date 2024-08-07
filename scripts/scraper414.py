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
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    data = []

    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, ".grid-job-holder a")
        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, '.grid-job .title h4').text.strip()
            except:
                continue
            link = item.get_attribute("href").strip()
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
