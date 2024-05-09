from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 390
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'a#hs-eu-decline-button').click()
    except:
        print("No Cookie Button")

    time.sleep(4)
    
    data = []
    
    try:
        items = driver.find_elements(By.CSS_SELECTOR, "div#vacancies-listing-results div.col-span-4")
    except:
        items = []

    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "h4").text.strip()
        if location in ['Birmingham', 'Glasgow', 'Brighton']:
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                    com,
                    f'{location}, United Kingdom',
                    link,
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
