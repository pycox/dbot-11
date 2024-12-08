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
    
    if "US" in locations:

        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "div#widget-jobsearch-results-list > div")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                location = item.find_element(By.CSS_SELECTOR, 'div.joblist-location').text.strip()

                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )
            
            try:
                button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Go to the next page of results."]')
                driver.execute_script("arguments[0].scrollIntoView();", button)
                driver.execute_script("arguments[0].click();", button)
                time.sleep(4)
            except Exception as e:
                flag = False
                print("No More Jobs", e)

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
