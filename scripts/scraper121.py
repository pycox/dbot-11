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
    time.sleep(2)

    items = driver.find_elements(
        By.CSS_SELECTOR, "ul li.list-item"
    )

    data = []

    if "UK" in locations:
        for item in items:
            data.append(
                [
                    driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "h2")).strip(),
                    com,
                    "UK",
                    url,
                ]
            )

    driver.quit()
    
    updateDB(key, data)


if __name__ == "__main__":
    main()
