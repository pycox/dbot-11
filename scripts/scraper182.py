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
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        time.sleep(4)

        try:
            driver.find_element(
                By.CSS_SELECTOR,
                "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
            ).click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        time.sleep(4)

        data = []

        total_count = int(
            driver.find_element(
                By.CSS_SELECTOR, ".pagination__count span:nth-child(2)"
            ).text.strip()
        )

        driver.find_element(
            By.CSS_SELECTOR, ".table.careers-vacancies-listing__table tr"
        )

        while total_count > 0:
            items = driver.find_elements(
                By.CSS_SELECTOR, ".table.careers-vacancies-listing__table tr"
            )
            for item in items[1:]:
                link = (
                    item.find_element(By.CSS_SELECTOR, "a")
                    .get_attribute("href")
                    .strip()
                )
                location = item.find_element(
                    By.CSS_SELECTOR, "td:nth-child(3) p:nth-child(2)"
                ).text.strip()

                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            try:
                total_count -= 15
                if total_count > 15:
                    button = driver.find_element(
                        By.CSS_SELECTOR, 'button[title="next"]'
                    )
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(4)
            except:
                total_count = 0

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
