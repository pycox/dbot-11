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
        driver.get(url)

        time.sleep(3)

        try:
            driver.find_element(
                By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"
            ).click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        data = []

        flag = True

        while flag:
            time.sleep(4)
            try:
                button = driver.find_element(By.CSS_SELECTOR, "#show-more-button")
                driver.execute_script("arguments[0].scrollIntoView();", button)
                driver.execute_script("arguments[0].click();", button)
            except Exception:
                flag = False

        driver.find_element(By.CSS_SELECTOR, "#talentlinkJobsList .job-list-tile")
        items = driver.find_elements(
            By.CSS_SELECTOR, "#talentlinkJobsList .job-list-tile"
        )

        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()

            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                    com,
                    "UK",
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
