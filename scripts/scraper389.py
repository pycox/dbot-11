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
    
    items = driver.find_elements(By.CSS_SELECTOR, "a.job-box-link.job-box")
    
    for item in items:
        location = item.find_element(By.CSS_SELECTOR, "span.multi-offices-desktop").text.strip()
        for str in locations:
            if (str in location):
                link = item.get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".jb-description span").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )
                break


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
