from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
    driver.switch_to.frame(iframe)

    items = driver.find_elements(By.CSS_SELECTOR, ".opening")

    data = []

    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        title = item.find_element(By.CSS_SELECTOR, "a").text.strip()
        location = (
            item.find_element(By.CSS_SELECTOR, ".location")
            .text
            .strip()
        )

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
