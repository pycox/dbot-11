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
    data = []
    regions = []
    
    if "UK" in locations:
        regions.append("United Kingdom")
    if "US" in locations:
        regions.append("United States")

    for location in regions:
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
