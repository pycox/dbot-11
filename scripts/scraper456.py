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
        driver.find_element(By.CSS_SELECTOR, '#onetrust-reject-all-handler').click()
    except:
        print("No Cookie Button")


    element = driver.find_element(By.CSS_SELECTOR, ".e-vacancies-list")
    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", element)

    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".e-vacancies-list a.e-vacancy-listing")
    for item in items:
        link = item.get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "p").text.strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
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
