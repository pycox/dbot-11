from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 326
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    time.sleep(4)
    data = []

    for location in ['United States', 'United Kingdom']:
        driver.find_element(By.CSS_SELECTOR, "#downshift-5-toggle-button").click()
        driver.find_element(By.CSS_SELECTOR, f'#downshift-5-menu li[aria-label="{location}"]').click()
        time.sleep(4)
        items = driver.find_elements(By.CSS_SELECTOR, ".sc-6exb5d-3.gnPPfQ")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                    com,
                    location,
                    link,
                ]
            )
        driver.find_element(By.CSS_SELECTOR, "div.sc-1vzxbt3-9.himVqE > div.sc-1vzxbt3-3.jIcLux > div.sc-1vzxbt3-4.sc-1up9u4w-0.glrEFW > button[type='button']").click()
        

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
