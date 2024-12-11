from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import updateDB, eventHander
import time


def main(key, com, url):
    options = Options()
    
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    
    data = []
    regions = []
    
    if "UK" in locations:
        regions.append(("London", "031b2e9d653801a327cde1b30a0126b5"))
    
    for location, location_id in regions:
        try:
            driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='distanceLocation']").click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, f"label[for='{location_id}']").click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='viewAllJobsButton'").click()
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
