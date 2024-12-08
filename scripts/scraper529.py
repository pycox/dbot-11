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
        driver.find_element(By.CSS_SELECTOR, 'button.cky-btn.cky-btn-reject').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    
    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, "li.elementor-icon-list-item a")
        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, "span b").text.strip()
            except:
                continue
            data.append(
                [
                    title,
                    com,
                    "UK",
                    item.get_attribute("href").strip(),
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
