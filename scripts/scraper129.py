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

        driver.find_element(
            By.CSS_SELECTOR, ".content-panel-container .content-panel.contact-block"
        )

        items = driver.find_elements(
            By.CSS_SELECTOR, ".content-panel-container .content-panel.contact-block"
        )

        data = []

        for item in items:
            location = item.find_element(
                By.CSS_SELECTOR, ".contact-header-pnl p"
            ).text.strip()

            sub_items = item.find_elements(By.CSS_SELECTOR, ".job-listings-block a")
            for sub_item in sub_items:
                data.append(
                    [
                        sub_item.text.strip(),
                        com,
                        location,
                        sub_item.get_attribute("href").strip(),
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
