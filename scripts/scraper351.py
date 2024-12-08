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
        driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler").click()
    except:
        print("No Cookie Button")

    time.sleep(4)

    data = []
    
    if "UK" in locations:
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".attrax-list-widget__list.attrax-list-widget__list--list.attrax-list-widget__list--has-items .attrax-vacancy-tile")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a[aria-label='Apply now']").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a.attrax-vacancy-tile__title").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next pagination page"]')
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
