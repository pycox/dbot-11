from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        data = []

        try:
            driver.find_element(By.CSS_SELECTOR, "button.acceptAllCookies").click()
            time.sleep(2)
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        try:
            driver.find_element(By.CSS_SELECTOR, 'li[data-term-id="248"]').click()
            driver.find_element(By.CSS_SELECTOR, 'li[data-term-id="239"]').click()
            driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Agree"]').click()
            driver.find_element(
                By.CSS_SELECTOR, 'label[for="ldReadDiscalimer2"]'
            ).click()
            button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Agree"]')
            driver.execute_script("arguments[0].click();", button)
        except:
            pass

        time.sleep(4)

        driver.find_element(
            By.CSS_SELECTOR, ".section__content .section__entry p span a"
        )
        items = driver.find_elements(
            By.CSS_SELECTOR, ".section__content .section__entry p span a"
        )

        for item in items:
            text = driver.execute_script("return arguments[0].innerText;", item)
            if not text:
                continue
            title, location = text.replace(">>", "").strip().split("-")
            link = item.get_attribute("href").strip()

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
