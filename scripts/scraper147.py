from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
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

    time.sleep(2)

    flag = True
    while flag:
        try:
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            showMore = driver.find_element(By.CSS_SELECTOR, "button[data-ui='load-more-button']")
            showMore.click()
            time.sleep(1)
        except Exception as e:
            flag = False
    time.sleep(4)

    items = driver.find_elements(By.CSS_SELECTOR, "li[data-ui='job']")
    data = []
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        title = item.find_element(By.CSS_SELECTOR, "h3[data-ui='job-title'] > span").text.strip()
        location = item.find_element(By.CSS_SELECTOR, "div[data-ui='job-location']").text.strip()
        for str in locations:
            if (str in location):
                data.append([
                    title,
                    com,
                    location,
                    link
                ])
                break

    updateDB(key, data)

if __name__ == "__main__":
    main()
    