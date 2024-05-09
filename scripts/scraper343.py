from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 343
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, ".Bloom__Tabs__tabsContainer___15dZB"))
    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, "div.Bloom__Tabs__tabContent___olq53.Bloom__Tabs__tabContentActive___amCL5 > div > div")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, "p").text.strip()
        location_ = location.lower()
        for str in ['london', 'new york', 'san francisco', 'united states', 'united kingdom', 'uk', 'usa', 'us']:
            if (str in location_):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
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
