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

    time.sleep(2)

    try:
        driver.find_element(By.CSS_SELECTOR, '.cookie-consent__button_accept').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)

    data = []
    regions = []
    
    if "US" in locations:
        regions.append("United States")
    if "UK" in locations:
        regions.append("United Kingdom")
    
    for location in regions:
        driver.get(f"{url}?location={location}")
        
        flag = True
        while flag:
            time.sleep(3)
            try:
                driver.find_element(By.CSS_SELECTOR, "#button_moreJobs").click()
            except Exception:
                flag = False
        
        items = driver.find_elements(By.CSS_SELECTOR, "li.direct_joblisting")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                    com,
                    location,
                    link,
                ]
            )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
