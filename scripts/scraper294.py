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
        driver.find_element(By.CSS_SELECTOR, "button.cf2Lf6.cf8Oal").click()
    except:
        print("No Cookie Button")

    time.sleep(4)

    data = []
    regions = []
    
    if "UK" in locations:
        regions.extend(["Winchester", "London", "Edinburgh"])
    
    for location in regions:
        Select(driver.find_element(By.CSS_SELECTOR, "select#locationsDropdown")).select_by_value(location)
        time.sleep(4)
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "#vacancieslisting .job-vacancies__job-container")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a.job-vacancies__job-more-button").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h2.job-vacancies__job-title").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            try:
                driver.find_element(By.CSS_SELECTOR, 'a[aria-label="next page"]').click()
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")

    driver.quit()
    updateDB(key, data)

if __name__ == "__main__":
    main()
