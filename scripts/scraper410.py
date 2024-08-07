from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    if url.endswith("/"):
        url = url[:-1]
    driver.get(url)

    time.sleep(4)

    data = []
    

    if "UK" in locations:    
        items = driver.find_elements(By.CSS_SELECTOR, ".jobListing__container a.jobPreview")
        for item in items:
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, ".xsTitle").text.strip(),
                    com,
                    "UK",
                    item.get_attribute("href"),
                ]
            )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
