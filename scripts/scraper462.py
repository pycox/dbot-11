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
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, '.decline.sqs-button-element--secondary.sqs-cookie-banner-v2-deny').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, "li.list-item")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "p")
        location = driver.execute_script("return arguments[0].innerText;", location).strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "h2")).strip(),
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
