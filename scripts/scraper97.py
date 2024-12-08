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
    driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary.oracletaleocwsv2-btn-fa.fa-search").click()
    time.sleep(4)
    
    items = driver.find_elements(By.CSS_SELECTOR, ".oracletaleocwsv2-accordion.oracletaleocwsv2-accordion-expandable.clearfix")

    data = []

    for item in items:
        location = item.find_elements(By.CSS_SELECTOR, 'div[tabindex="0"]')[1].text.strip()
        for str in locations:
            if (str in location):   
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
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
