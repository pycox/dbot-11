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

    time.sleep(3)

    try:
        driver.find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    
    flag = True
    while flag:
        time.sleep(4)
        try:
            button = driver.find_element(By.CSS_SELECTOR, "button.border-accent.text-accent")
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
        except Exception as e:
            print(e)
            flag = False
    
    items = driver.find_elements(By.CSS_SELECTOR, ".relative .grid a")
    for item in items:
        link = item.get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, ".flex.items-center.gap-4 div:nth-child(3)").text.strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
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
