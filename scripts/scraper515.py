from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    data = []
    
    time.sleep(4)
    try:
        driver.find_element(By.CSS_SELECTOR, '#hs-eu-confirmation-button').click()
    except:
        print("No Cookie Button")
    time.sleep(2)
    
    flag = True
    while flag:
        time.sleep(4)
        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                flag = False
        except:
            flag = False

    items = driver.find_elements(By.CSS_SELECTOR, ".container-jobs .item-job")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, ".city-job p").text.strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h5").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )
                break


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
