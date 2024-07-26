from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(4)

    data = []

    flag = True

    if "UK" in locations:
        while flag:
                
            items = driver.find_elements(By.CSS_SELECTOR, "div.vsr-job")
            
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "h3.vsr-job__title > a").get_attribute('href')
                title = item.find_element(By.CSS_SELECTOR, "h3.vsr-job__title > a").text.strip()
                location = item.find_element(By.CSS_SELECTOR, "div[data-id='div_content_VacV_LocationID'] > span").text.strip()
                data.append([
                    title,
                    com,
                    location,
                    link
                ])


            try:
                button = driver.find_element(By.XPATH, "//a[text()='Next']")
                driver.execute_script("arguments[0].click();", button)
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")


    updateDB(key, data)

if __name__ == "__main__":
    main()
    