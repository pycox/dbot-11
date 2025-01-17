from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import updateDB, eventHander
import time


def main(key, com, url):
    options = Options()

    options.add_argument("--log-level=3")
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        time.sleep(2)

        try:
            driver.find_element(
                By.CSS_SELECTOR,
                "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
            ).click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        time.sleep(2)

        data = []

        regions = ["United Kingdom", "United States"]

        for region in regions:
            Select(
                driver.find_element(By.CSS_SELECTOR, "select#careers_filter_dropdown")
            ).select_by_value(region)
            driver.find_element(
                By.CSS_SELECTOR, 'input[value="Update results"]'
            ).click()
            time.sleep(4)

            flag = True

            while flag:
                items = driver.find_elements(
                    By.CSS_SELECTOR, ".careers-search .careers-featured-cards"
                )
                for item in items:
                    link = (
                        item.find_element(By.CSS_SELECTOR, "a")
                        .get_attribute("href")
                        .strip()
                    )
                    title = driver.execute_script(
                        "return arguments[0].innerText;",
                        item.find_element(By.CSS_SELECTOR, "h3"),
                    )

                    data.append(
                        [
                            title.strip(),
                            com,
                            region,
                            link,
                        ]
                    )

                try:
                    driver.find_element(
                        By.CSS_SELECTOR, "a.px-4.py-2.border.bg-white.leading-2"
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
