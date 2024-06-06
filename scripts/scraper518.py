from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 518
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(2)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".e-con.e-child .e-con-inner")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a.elementor-button.elementor-button-link.elementor-size-sm").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "p.elementor-heading-title.elementor-size-default").text.strip()
        for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
            if (str in location):
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
