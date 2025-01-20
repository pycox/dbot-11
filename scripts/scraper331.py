from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time
from bs4 import BeautifulSoup


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
        time.sleep(2)
        driver.get(url)
        time.sleep(3)

        data = []

        try:
            driver.find_element(
                By.CSS_SELECTOR,
                "button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')]",
            ).click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        soup = BeautifulSoup(driver.page_source, "html.parser")

        items = soup.select(".careers-list__row")[1:]

        for item in items:
            link = item.find("a").get("href").strip()
            location = item.select_one(".careers-list__col:nth-child(3)").text.strip()

            data.append(
                [
                    item.select_one(".careers-list__col:nth-child(1)").text.strip(),
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
