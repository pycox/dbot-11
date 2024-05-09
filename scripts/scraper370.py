from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 370
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    Select(driver.find_element(By.CSS_SELECTOR, "select#edit-field-position-type-value")).select_by_value("5")
    
    time.sleep(4)
    
    driver.find_element(By.CSS_SELECTOR, 'input#edit-submit-jobs').click()
    
    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".views-table.views-view-table.cols-3 tbody tr")
    
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "td:nth-child(1) a").get_attribute("href").strip()
        location = "US"
        data.append(
            [
                item.find_element(By.CSS_SELECTOR, "td:nth-child(1) a").text.strip(),
                com,
                location,
                link,
            ]
        )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
