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
        driver.find_element(By.CSS_SELECTOR, '.c-button.js-cookie-consent').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".c-card.c-card--job")
        for item in items:
            try:
                location = item.find_element(By.CSS_SELECTOR, "li:nth-child(1)").text.strip()
            except:
                continue
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                            com,
                            location,
                            item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip(),
                        ]
                    )
                    break

        try:
            button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next page"]')
            if not button.get_attribute("href"):
                flag = False
            else:
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
