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
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://3smoney-1653552517.teamtailor.com/jobs")

        data = []

        driver.implicitly_wait(8)

        driver.find_element(By.CSS_SELECTOR, "li.block-grid-item")
        items = driver.find_elements(By.CSS_SELECTOR, "li.block-grid-item")

        for item in items:

            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            location_elements = item.find_elements(
                By.CSS_SELECTOR, "div.mt-1.text-md > span"
            )
            location = (
                location_elements[-3].text.strip()
                if len(location_elements) > 2
                else "Location not available"
            )

            data.append(
                [
                    item.find_element(
                        By.CSS_SELECTOR, "span.text-block-base-link.company-link-style"
                    ).get_attribute("title"),
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
