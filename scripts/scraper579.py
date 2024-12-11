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

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(3)
    try:
        button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Last"]')
        driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(3)
    except Exception:
        print("No Last Page")
        
    
    time.sleep(3)

    data = []
    
    if "UK" in locations:
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".search-results-list .list-group")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'li[title="Previous"]')
                if "ng-hide" in next_button.get_attribute("class"):
                    flag = False
                else:
                    next_button.find_element(By.CSS_SELECTOR, 'a').click()
                    
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
