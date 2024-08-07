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

    data = []

    try:
        driver.find_element(By.CSS_SELECTOR, '#ppms_cm_reject-all').click()
    except:
        print("No Cookie Button")

    items = driver.find_elements(By.CSS_SELECTOR, ".XHfit")
    for item in items:
        driver.execute_script("arguments[0].scrollIntoView();", item)
        driver.execute_script("arguments[0].click();", item)
        item = item.find_element(By.XPATH, "..")
        sub_items = item.find_elements(By.CSS_SELECTOR, ".ccbLYr")
        for sub_item in sub_items:
            link = sub_item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = sub_item.find_elements(By.CSS_SELECTOR, "span")[1].text.strip()
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            sub_item.find_element(By.CSS_SELECTOR, "a span").text.strip(),
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
