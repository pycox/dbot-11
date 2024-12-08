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

    active_page = 1
    total_page = int(driver.find_elements(By.CSS_SELECTOR, ".c-jobs-listing__pagination-link")[-1].text.strip())

    while total_page > active_page:
        
        items = driver.find_elements(By.CSS_SELECTOR, "div.c-jobs-listing__item")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, 'div.c-jobs-listing__detail.c-jobs-listing__detail--location').text.strip()

            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break
        
        try:
            active_page += 1
            button = driver.find_elements(By.CSS_SELECTOR, ".c-jobs-listing__pagination-link")[active_page-1]
            driver.execute_script("arguments[0].click();", button)
            time.sleep(4)
        except:
            active_page = total_page + 1
            print("No More Jobs")

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
