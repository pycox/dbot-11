from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time


def main(key, com, url):
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        time.sleep(4)

        data = []

        driver.find_element(By.CSS_SELECTOR, "li.whr-item")
        items = driver.find_elements(By.CSS_SELECTOR, "li.whr-item")

        for item in items:
            link_tag = item.find_element(By.TAG_NAME, "a")
            link = link_tag.get_attribute("href") if link_tag else ""

            location_tag = item.find_element(By.CSS_SELECTOR, "li.whr-location")
            location = location_tag.text.strip() if location_tag else ""

            title_tag = item.find_element(By.TAG_NAME, "h3")
            title = title_tag.text.strip() if title_tag else ""

            data.append(
                [
                    title,
                    com,
                    location,
                    link,
                ]
            )

        updateDB(key, data)
    except Exception as e:
        print(key, "========", e)
        if "ERR_CONNECTION_TIMED_OUT" in str(e):
            eventHander(key, "CONNFAILED")
        elif "no such element" in str(e):
            eventHander(key, "UPDATED")
        elif "ERR_NAME_NOT_RESOLVED" in str(e):
            eventHander(key, "CONNFAILED")
        else:
            eventHander(key, "UNKNOWN")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
