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

    time.sleep(5)

    data = []
    regions = []

    if "UK" in locations:
        regions.append(("3440200Di4", "United Kingdom"))
    
    for location_code, location in regions:
        Select(driver.find_element(By.CSS_SELECTOR, "select#region")).deselect_all()
        Select(driver.find_element(By.CSS_SELECTOR, "select#region")).select_by_value(location_code)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "input[value=\"Search\"]").click()
        time.sleep(4)
        
        flag = True
        
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "tr td h2 a")
            for item in items:
                link = item.get_attribute("href").strip()
                title = driver.execute_script("return arguments[0].innerText;", item)
                data.append(
                    [
                        title.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]')
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")
                
        driver.get(url)
        time.sleep(5)
        
    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
