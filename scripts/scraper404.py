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
    
    try:
        driver.find_element(By.CSS_SELECTOR, '#CybotCookiebotDialogBodyButtonDecline').click()
    except:
        print("No Cookie Button")
    time.sleep(2)
        
    if "UK" in locations:
        regions.append(("United Kingdom", ".CodeListEntryId_10"))
    if "US" in locations:
        regions.append(("United States", ".CodeListEntryId_386"))

    for location, location_class in regions:
        button = driver.find_element(By.CSS_SELECTOR, location_class)
        driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(4)
        
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".ListGridContainer .rowContainerHolder")
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
            
    
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, '.pagingButtons a.scroller_movenext')
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                if next_button.get_attribute("disabled") == "disabled":
                    flag = False
                else:
                    next_button.click()

                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")      
        
        button = driver.find_element(By.CSS_SELECTOR, location_class)
        driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(3)

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
