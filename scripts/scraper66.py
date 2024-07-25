from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(10)
    try:
        driver.find_element(By.CSS_SELECTOR, "a#LOCATION-moreless").click()
    except Exception as e:
        print(f"Scraper{key}: {e}")
    time.sleep(4)
    
    locations = []
    if "US" in locations:
        try:
            driver.find_element(
                By.XPATH, "//span[contains(text(), 'United States')]"
            ).click()
        except Exception as e:
            print(f"Scraper{key}: {e}")
        time.sleep(4)
    
    if "UK" in locations:
        try:
            driver.find_element(
                By.XPATH, "//span[contains(text(), 'United Kingdom')]"
            ).click()
        except Exception as e:
            print(f"Scraper{key}: {e}")
        time.sleep(8)

    data = []

    items = driver.find_elements(By.CSS_SELECTOR, "tbody.jobsbody tr")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        location = item.find_elements(By.CSS_SELECTOR, "td")[1].text.strip()
        data.append(
            [
                item.find_element(By.CSS_SELECTOR, "th").text.strip(),
                com,
                location,
                link,
            ]
        )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
