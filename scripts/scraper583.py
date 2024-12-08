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

    time.sleep(3)

    try:
        driver.find_element(By.CSS_SELECTOR, '.cc-btn.cc-allow').click()
    except:
        print("No Cookie Button")
    time.sleep(3)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    curr_page = '0'
    
    if "UK" in locations:
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "a.iemdmt")
            for item in items:
                link = item.get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )
                
            try:
                current = driver.find_element(By.CSS_SELECTOR, 'span.current').text.strip()
                if current == curr_page:
                    flag = False
                else:
                    curr_page = current
                    button = driver.find_element(By.CSS_SELECTOR, '.gFRci:nth-child(3)')
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(4)
            except Exception:
                flag = False
                print("No More Jobs")

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
