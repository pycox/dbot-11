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

    time.sleep(4)

    data = []
    
    if "UK" in locations:
    
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "ol#jobsListParent li .job-card")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".job-title").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, '#paginationHolder a[rel="next"]')
                next_button.click()
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
