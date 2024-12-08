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
        driver.find_element(By.CSS_SELECTOR, "#igdpr-reject-button").click()
    except:
        print("No Cookie Button")

    data = []
    regions = []

    if "UK" in locations:
        regions.append("United Kingdom")

    if "US" in locations:
        regions.append("United States")
        
        
    button = driver.find_element(By.CSS_SELECTOR, "#country-toggle")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)
    button = driver.find_element(By.CSS_SELECTOR, f"input[data-display=\"{regions[0]}\"]")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    driver.execute_script("arguments[0].click();", button)   
    time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR, "#country-toggle")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)
    for location in regions:
        try:
            button = driver.find_element(By.CSS_SELECTOR, f"input[data-display=\"{location}\"]")
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(5)
        except Exception:
            continue
        
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "ul.job-list li.job-list__item")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(2)
                if "disabled" in next_button.get_attribute("class"):
                    flag = False
                else:
                    next_button.click()
                time.sleep(4)
            except Exception:
                flag = False
                print("No More Jobs")
        
        try:
            button = driver.find_element(By.CSS_SELECTOR, f"input[data-display=\"{location}\"]")
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(5)
        except Exception:
            continue

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
