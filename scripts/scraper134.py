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

    items = driver.find_elements(By.CSS_SELECTOR, "#job-list h4")
    url_ = url.split("#")[0]
    data = []

    for item in items:
        job_id = item.find_element(By.CSS_SELECTOR, "button").get_attribute("id").strip()
        link = f"{url_}#{job_id}"
        location = item.find_elements(By.CSS_SELECTOR, 'span span')[0].text.strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_elements(By.CSS_SELECTOR, 'span span')[1].text.strip(),
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
