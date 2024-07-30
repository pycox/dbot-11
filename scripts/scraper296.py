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
    

    if "UK" in locations:
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".article-list .article-body")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "div.readmore a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".article-header h2 a").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                driver.find_element(By.CSS_SELECTOR, 'a.page-link.next').click()
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
