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

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        data = []
        curr_page = "0"

        flag = True

        driver.find_element(By.CSS_SELECTOR, "a.iemdmt")

        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "a.iemdmt")

            for item in items:
                link = item.get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                current = driver.find_element(
                    By.CSS_SELECTOR, "span.current"
                ).text.strip()
                if current == curr_page:
                    flag = False
                else:
                    curr_page = current
                    button = driver.find_element(By.CSS_SELECTOR, ".gFRci:nth-child(3)")
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(4)
            except Exception:
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
