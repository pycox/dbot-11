from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 508
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".availablerole")
    for item in items:
        try:
            title = driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, ".jobtitle"))
        except:
            continue
        if title:
            data.append(
                [
                    title.strip(),
                    com,
                    "UK",
                    item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                ]
            )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
