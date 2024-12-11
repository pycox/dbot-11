from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    
    try:
        driver.find_element(By.CSS_SELECTOR, '._brlbs-refuse-btn').click()
    except:
        print("No Cookie Button")

    time.sleep(4)

    data = []
    

    if "UK" in locations:
        
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
        driver.switch_to.frame(iframe)

        search_field = driver.find_element(By.CSS_SELECTOR, "input#geoLocation_search")
        driver.execute_script("arguments[0].scrollIntoView();", search_field)
        time.sleep(2)
        search_field.send_keys("UK")
        search_field.send_keys(Keys.ENTER)
        time.sleep(4)
        
        items = driver.find_elements(By.CSS_SELECTOR, ".outputContainer .matchElement:not([style*='display: none'])")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "a")).strip(),
                    com,
                    "UK",
                    link,
                ]
            )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
