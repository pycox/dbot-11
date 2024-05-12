from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 511
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url.strip())

    time.sleep(4)
    
    try:
        driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler").click()
    except:
        print("No Cookie Button")
    data = []
    
    driver.find_element(By.CSS_SELECTOR, 'a[title="Button View Open Positions"]').click()
    time.sleep(4)
        
    for location, location_id in [("United States", "bc33aa3152ec42d4995f4791a106ed09"), ("United Kingdom", "29247e57dbaf46fb855b224e03170bc7")]:
        try:
            driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='distanceLocation']").click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, "label[for='location']").click()
            time.sleep(2)
            driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, f"input#{location_id}"))
            driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='sidebar'").click()
            
            time.sleep(3)
        except:
            continue

        flag = True

        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            
            try:
                driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, 'button[data-uxi-element-id="next"]'))
                
                time.sleep(4)
            except Exception:
                flag = False
                print("No More Jobs")
        
        try:
            driver.find_element(By.CSS_SELECTOR, 'button[data-automation-id="clearAllButton"]').click()
        except:
            print("No filter to clear")

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
