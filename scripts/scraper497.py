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
        driver.find_element(By.CSS_SELECTOR, 'button#onetrust-reject-all-handler').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, ".cards"))
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".cards .card a")
    for item in items:
        link = item.get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "p").text.split("\n")[0].strip()
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
