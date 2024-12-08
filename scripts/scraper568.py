from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import updateDB, eventHander
import time

def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, '.cky-btn.cky-btn-accept').click()
    except:
        print("No Cookie Button")

    time.sleep(4)

    data = []
    regions = []
    
    if "UK" in locations:
        regions.append(("UK", "9307855"))
    
    if "US" in locations:
        regions.append(("US", "9307859"))
    
    for location, location_code in regions:
        driver.get(f"{url}/{location_code}")
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".job_list_row .jlr_title a")
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
                curr_button = int(driver.find_element(By.CSS_SELECTOR, '.pagination span[aria-label="current"]').text.strip())
                next_button = driver.find_element(By.CSS_SELECTOR, f'.pagination a[data-page="{curr_button+1}"]')
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
