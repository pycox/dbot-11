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

    try:
        driver.find_element(By.CSS_SELECTOR, "input.js-consent-all-submit").click()
    except Exception as e:
        print(f"Scraper{key} cookie Button: {e}")

    flag = True
    data = []

    while flag:
        try:
            time.sleep(4)

            # nextBtn = driver.find_elements(By.CSS_SELECTOR, "a.next")

            if len(driver.find_elements(By.CSS_SELECTOR, "a.oj-joblist-more")) > 0:
                element = driver.find_element(By.CSS_SELECTOR, "ul.dgt-list-items")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
                # nextBtn[0].click()
            else:
                flag = False
        except:
            flag = False

    time.sleep(4)

    items = driver.find_elements(By.CSS_SELECTOR, "ul.dgt-list-items > li")[:-1]

    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        location = item.find_element(By.CSS_SELECTOR, "span.location").text.strip()

        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "span.title").text.strip(),
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
