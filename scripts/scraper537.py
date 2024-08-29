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

    time.sleep(3)
    
    try:
        driver.find_element(By.CSS_SELECTOR, '#cookie-accept').click()
    except:
        print("No Cookie Button")

    time.sleep(3)
    
    data = []
    regions = []

    if "UK" in locations:
        regions.append("United Kingdom")
    
    if "US" in locations:
        regions.append("United States")    
    
    for location in regions:
        driver.get(f"{url}?&locationsearch={location}")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "#searchresults tbody tr a.jobTitle-link")
            for item in items:
                link = item.get_attribute("href").strip()
                data.append(
                    [
                        driver.execute_script("return arguments[0].innerText;", item).strip(),
                        com,
                        location,
                        link,
                    ]
                )
            try:
                curr_button = int(driver.find_element(By.CSS_SELECTOR, 'ul.pagination li a.current-page').text.strip())
                next_button = driver.find_element(By.CSS_SELECTOR, f'ul.pagination li a[title="Page {curr_button+1}"]')
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
