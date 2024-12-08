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
    time.sleep(3)

    try:
        driver.find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler').click()
    except:
        print("No Cookie Button")

    data = []
    regions = []
    
    if "UK" in locations:
        regions.append(("United Kingdom", "united-kingdom"))
    if "US" in locations:
        regions.append(("United States of America", "united-states"))
    
    for location, location_slug in regions:
        driver.get(f"{url}{location_slug}")
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "li.job-result-item")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".job-title").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            try:
                button = driver.find_element(By.CSS_SELECTOR, 'li[data-pagination="next"] a')
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
