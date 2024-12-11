from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
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

    time.sleep(3)

    try:
        driver.find_element(By.CSS_SELECTOR, '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, "h5 strong")
    for item in items:
        location = item.text.strip()
        if location not in locations:
            continue
        try:
            item = item.find_element(By.XPATH, './../following-sibling::ul')
            if not item:
                continue
        except Exception:
            continue
        for sub_item in item.find_elements(By.CSS_SELECTOR, "li a"):
            data.append(
                [
                    sub_item.text.strip(),
                    com,
                    location,
                    sub_item.get_attribute("href").strip(),
                ]
            )
    
    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
