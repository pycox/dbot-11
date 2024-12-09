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

        try:
            driver.find_element(
                By.CSS_SELECTOR,
                "button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
            ).click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        time.sleep(4)

        data = []

        tmp = driver.find_elements(
            By.XPATH,
            "//p[contains(text(), 'There are no vacancies at the moment. Please follow us and subscribe for new opportunities.')]",
        )

        if len(tmp):
            updateDB(key, data)
            return

        driver.find_element(By.CSS_SELECTOR, 'a[data-heap-component="card-internal"]')
        items = driver.find_elements(
            By.CSS_SELECTOR, 'a[data-heap-component="card-internal"]'
        )

        for item in items:
            link = item.get_attribute("href")
            title, location = item.find_element(By.CSS_SELECTOR, "h2").text.split(",")

            data.append(
                [
                    title.strip(),
                    com,
                    location.strip(),
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
