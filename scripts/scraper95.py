from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
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

        try:
            driver.find_element(
                By.CSS_SELECTOR, "button[data-automation-id='legalNoticeDeclineButton']"
            ).click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        time.sleep(4)

        data = []

        flag = True

        driver.find_element(By.CSS_SELECTOR, "li.css-1q2dra3")

        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
            for item in items:
                link = (
                    item.find_element(By.CSS_SELECTOR, "h3 a")
                    .get_attribute("href")
                    .strip()
                )
                try:
                    location = item.find_element(
                        By.CSS_SELECTOR, ".css-248241 .css-129m7dg"
                    ).text.strip()
                except:
                    continue

                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            try:
                driver.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="next"]'
                ).click()
                time.sleep(4)
            except:
                flag = False

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
