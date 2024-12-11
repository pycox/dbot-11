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

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button[data-action="click->common--cookies--alert#disableAll"]').click()
    except:
        print("No Cookie Button")
    
    time.sleep(2)
    data = []
    
    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, "#jobs_list_container li a")
        for item in items:
            link = item.get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "span.company-link-style").text.strip(),
                    com,
                    "UK",
                    link,
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
