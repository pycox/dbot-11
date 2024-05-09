from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 335
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button#didomi-notice-disagree-button').click()
    except:
        print("No Cookie Button")

    data = []
    
    for location, location_code in [("London", 2862), ("UK", 3033)]:
        driver.get(f"{url}?facet_JobCountry={location_code}")
        time.sleep(4)
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".ts-offer-card")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            try:
                driver.find_element(By.CSS_SELECTOR, 'a[title="Next page of results"]').click()
                time.sleep(4)
            except:
                flag = False

        driver.get(f"{url}?facet_JobCountry=-{location_code}")
        time.sleep(4)


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
