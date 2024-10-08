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

    data = []
    
    time.sleep(4)
    
    if "UK" in locations:
        flag = True
        while flag:
            time.sleep(4)
            try:
                last_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    flag = False
            except:
                flag = False

        items = driver.find_elements(By.CSS_SELECTOR, "#results .vacancy-search-result-item a.apply-link")
        for item in items:
            link = item.get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                    com,
                    "UK",
                    link,
                ]
            )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
