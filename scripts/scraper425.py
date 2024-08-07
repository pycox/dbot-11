from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    
    try:
        driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='legalNoticeDeclineButton']").click()
    except:
        print("No Cookie Button")

    data = []
    regions = []

    if "UK" in locations:
        regions.append(("United Kingdom", "29247e57dbaf46fb855b224e03170bc7"))

    if "US" in locations:
        regions.append(("United States", "bc33aa3152ec42d4995f4791a106ed09"))
        
    for location, location_id in regions:
        try:
            driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='distanceLocation']").click()
            time.sleep(3)
            element = driver.find_element(By.CSS_SELECTOR, ".css-vdogor:nth-child(3) .ReactVirtualized__List")
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", element)
            time.sleep(2)
            button = driver.find_element(By.CSS_SELECTOR, f"label[for='{location_id}']")
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
            driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='sidebar']").click()
            time.sleep(3)
        except Exception:
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
                button = driver.find_element(By.CSS_SELECTOR, 'button[data-uxi-element-id="next"]')
                driver.execute_script("arguments[0].scrollIntoView();", button)
                driver.execute_script("arguments[0].click();", button)
                time.sleep(4)
            except Exception:
                flag = False
                print("No More Jobs")
        
        try:
            driver.find_element(By.CSS_SELECTOR, 'button[data-automation-id="clearAllButton"]').click()
            time.sleep(4)
        except:
            print("No filter to clear")

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
