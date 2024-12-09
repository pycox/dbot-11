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
        flag = True

        driver.find_elements(By.CSS_SELECTOR, 'li[data-ui="job"]')

        while flag:
            try:
                time.sleep(4)

                driver.find_element(
                    By.CSS_SELECTOR, 'button[data-ui="load-more-button"]'
                ).click()

            except Exception as e:
                flag = False
                break

        driver.find_element(By.CSS_SELECTOR, 'li[data-ui="job"]')
        items = driver.find_elements(By.CSS_SELECTOR, 'li[data-ui="job"]')

        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            title = item.find_element(By.CSS_SELECTOR, "h3").text.strip()
            location = item.find_element(
                By.CSS_SELECTOR, 'div[data-ui="job-location"]'
            ).text.strip()

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
