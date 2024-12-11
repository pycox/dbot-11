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

    time.sleep(3)
    try:
        driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler').click()
    except:
        print("No Cookie Button")
    time.sleep(3)

    data = []
    regions = []

    if "UK" in locations:
        regions.append(("4732532", "United Kingdom"))
    
    if "US" in locations:
        regions.append(("4732533", "United State"))    
    
    for location_code, location in regions:
        
        driver.get(f"{url}?1331={location_code}")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".article.article--result h2 a")
            for item in items:
                data.append(
                    [
                        item.text.strip(),
                        com,
                        location,
                        item.get_attribute("href").strip(),
                    ]
                )
            
            try:
                button = driver.find_element(By.CSS_SELECTOR, 'a.list-controls__pagination__item.paginationNextLink')
                driver.execute_script("arguments[0].scrollIntoView();", button)
                driver.execute_script("arguments[0].click();", button)
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
