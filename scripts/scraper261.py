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

    data = []
    flag = True

    try:
        driver.find_element(By.CSS_SELECTOR, "button#onetrust-reject-all-handler").click()
    except:
        print("No Cookie button")

    if "UK" in locations:
        while flag:
            time.sleep(4)
            items = driver.find_elements(By.CSS_SELECTOR, "ul > li.c-job-listing-card")

            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "p.c-job-listing-card__header").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                driver.find_element(By.CSS_SELECTOR, "a.c-job-listing-left__right-arrow").click()
            except:
                flag = False
                print("No more Jobs")

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
