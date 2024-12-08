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

    data = []
    regions = []
    
    if "UK" in locations:
        regions.extend(['London', 'United Kingdom', 'UK'])

    if "US" in locations:
        regions.extend(['New York', 'San Francisco', 'United States', 'USA', 'US'])


    countries = driver.find_elements(By.CSS_SELECTOR, "div.positions--country")
    for country in countries:
        country_name = country.find_element(By.CSS_SELECTOR, "h2").text.strip()
        if country_name in regions:

            items = country.find_elements(By.CSS_SELECTOR, "div.positions-items > div.positions--card")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()

                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                        com,
                        country_name,
                        link,
                    ]
                )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
