from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 540
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(2)

    data = []
    
    flag = True
    while flag:
        time.sleep(4)
        try:
            driver.find_element(By.CSS_SELECTOR, "#show_more_button").click()
        except Exception:
            flag = False
    
    items = driver.find_elements(By.CSS_SELECTOR, "#jobs_list_container li")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, ".mt-1.text-md").text
        for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom']:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "span.company-link-style").text.strip(),
                        com,
                        str,
                        link,
                    ]
                )
                break


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
