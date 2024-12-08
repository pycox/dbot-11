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

    data = []
    
    try:
        driver.find_element(By.CSS_SELECTOR, 'a.eu-cookie-compliance-rocketship--accept-minimal.button').click()
    except:
        print("No Cookie Button")
    
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".group.views-element-container .view__content .views__row")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".field--name-field-country").text.strip()
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break

        try:
            curr_button = int(driver.find_element(By.CSS_SELECTOR, 'a.pager__link.is-active').text.split("\n")[-1].strip())
            next_button = driver.find_element(By.CSS_SELECTOR, f'a.pager__link[title="Go to page {curr_button+1}"]')
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(4)
        except Exception:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
