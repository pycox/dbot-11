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

        flag = True
        data = []

        time.sleep(8)

        try:
            driver.find_element(
                By.CSS_SELECTOR, 'button[aria-label="Yes, I agree"]'
            ).click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        driver.find_element(
            By.CSS_SELECTOR, ".wpb_column.vc_column_container.our_jobs_item"
        )

        while flag:
            time.sleep(4)
            items = driver.find_elements(
                By.CSS_SELECTOR, ".wpb_column.vc_column_container.our_jobs_item"
            )

            for item in items:
                link = (
                    item.find_element(By.CSS_SELECTOR, "a")
                    .get_attribute("href")
                    .strip()
                )
                location = item.find_element(
                    By.CSS_SELECTOR, ".joblocation"
                ).text.strip()

                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            try:
                driver.find_element(
                    By.CSS_SELECTOR, "main#main a.next.page-numbers > span"
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
