from selenium import webdriver
from selenium.webdriver.common.by import By
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

    time.sleep(4)

    try:
        driver.find_element(
            By.XPATH, "//button[contains(text(), 'accept all cookies')]"
        ).click()
    except Exception as e:
        print(f"Scraper{key} cookie Button: {e}")

    time.sleep(4)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(4)

    items = driver.find_elements(By.CSS_SELECTOR, "a.jk--link--text")

    data = []

    if "UK" in locations:
        for item in items:
            link = item.get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "div.title").text.strip(),
                    com,
                    "United Kingdom",
                    link,
                ]
            )

    driver.quit()
    
    updateDB(key, data)


if __name__ == "__main__":
    main()
