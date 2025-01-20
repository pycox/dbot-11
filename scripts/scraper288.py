from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        data = []

        flag = True

        driver.find_element(By.CSS_SELECTOR, "li.related-card")

        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "li.related-card")

            for item in items:
                link = (
                    item.find_element(By.CSS_SELECTOR, "a")
                    .get_attribute("href")
                    .strip()
                )
                location = item.find_element(
                    By.CSS_SELECTOR, "dd.location"
                ).text.strip()

                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            try:
                links = driver.find_elements(By.CSS_SELECTOR, ".pagingPanel a")
                next_page = links[-2]
                if next_page.text.strip() == "Next":
                    driver.execute_script("arguments[0].click();", next_page)
                else:
                    flag = False

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
