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
        driver.find_element(By.CSS_SELECTOR, 'button#cookie-acknowledge').click()
    except:
        print("No Cookie Button")

    time.sleep(4)

    data = []
    regions = []
    
    if "UK" in locations:
        regions.append(("UK", "GB"))
    
    if "US" in locations:
        regions.append(("US", "US"))
    
    for location, location_code in regions:
        driver.get(f"{url}?optionsFacetsDD_country={location_code}")
        time.sleep(4)
        
        flag = True
        while flag:
            try:
                driver.find_element(By.CSS_SELECTOR, "#tile-more-results").click()
                time.sleep(7)
            except Exception:
                flag = False
        
        items = driver.find_elements(By.CSS_SELECTOR, ".row.job.job-row")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, ".tiletitle a").text.strip(),
                    com,
                    location,
                    link,
                ]
            )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
