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

        time.sleep(4)

        try:
            driver.find_element(
                By.XPATH, "//button[contains(text(), 'Accept all cookies')]"
            ).click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        time.sleep(2)

        dom = driver.find_element(By.CSS_SELECTOR, "ul#jobs_list_container")

        dom.find_element(By.CSS_SELECTOR, "li")
        items = dom.find_elements(By.CSS_SELECTOR, "li")

        data = []

        for item in items:
            location = item.find_elements(By.CSS_SELECTOR, ".mt-1.text-md span")[
                -3
            ].text.strip()
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()

            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "span").text.strip(),
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
