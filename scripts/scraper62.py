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

    time.sleep(8)

    try:
        driver.find_element(
            By.CSS_SELECTOR,
            "button#accept-recommended-btn-handler",
        ).click()
    except Exception as e:
        print(f"Scraper{key} cookiee button: {e}")
        
    time.sleep(4)

    items = driver.find_elements(By.CSS_SELECTOR, "a.job-offer")

    data = []

    for item in items:
        link = item.get_attribute("href").strip()
        location = item.find_element(
            By.CSS_SELECTOR, "p.job-offer__location"
        ).text.strip()

        for str in locations:
            if str in location:
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "p").text.strip(),
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
