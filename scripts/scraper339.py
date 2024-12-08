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

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button#onetrust-reject-all-handler').click()
    except:
        print("No Cookie Button")

    time.sleep(2)

    data = []
    
    flag = True
    while flag:
        try:
            driver.execute_script("arguments[0].scrollIntoView(); window.scrollBy(0, -100);", driver.find_element(By.CSS_SELECTOR, "a.block-job-search__results-load"))
            driver.find_element(By.CSS_SELECTOR, "a.block-job-search__results-load").click()
            time.sleep(4)
        except Exception:
            flag = False
            print("No more page")
    
    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, "li.block-job-search__result")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, ".block-job-search__result-title").text.strip(),
                    com,
                    "UK",
                    link,
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
