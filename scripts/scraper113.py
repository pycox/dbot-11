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

        time.sleep(2)

        data = []

        flag = True

        driver.find_element(By.CSS_SELECTOR, "#search-results-list li a")

        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "#search-results-list li a")
            driver.find_elements(By.CSS_SELECTOR, "#search-results-list li a")

            for item in items:
                link = item.get_attribute("href").strip()
                title = driver.execute_script(
                    "return arguments[0].innerText;",
                    item.find_element(By.CSS_SELECTOR, "h3"),
                )

                data.append(
                    [
                        title.strip(),
                        com,
                        driver.execute_script(
                            "return arguments[0].innerText;",
                            item.find_element(By.CSS_SELECTOR, "span.job-location"),
                        ),
                        link,
                    ]
                )

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
                if "disable" in next_button.get_attribute("class"):
                    flag = False
                else:
                    driver.execute_script("arguments[0].click();", next_button)

                time.sleep(4)
            except Exception as e:
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
