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

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        time.sleep(4)
        try:
            driver.find_element(By.CSS_SELECTOR, "button[title=\"See more\"]").click()
        except Exception:
            flag = False
    
    items = driver.find_elements(By.CSS_SELECTOR, "a[data-testid=\"jobListItem\"]")
    for item in items:
        link = item.get_attribute("href").strip()
        location = item.find_elements(By.CSS_SELECTOR, "span")[1].text.strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
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
