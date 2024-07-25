from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(6)

    data = []
    
    regions = []
    if "UK" in locations:
        regions.append("United Kingdom")
    if "US" in locations:
        regions.append("United States")
    for region in regions:
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, f'div#CountryFacet label input[aria-label="{region}"]'))
        time.sleep(4)
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, "#j-careers-search__results .c-careers-search__list-item")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".location-field p").text.strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h6").text.strip(),
                    com,
                    location,
                    link,
                ]
            )

        try:
            driver.find_element(By.CSS_SELECTOR, 'a.c-careers-search__page-next').click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
