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

        data = []

        driver.find_element(
            By.CSS_SELECTOR, "a.elementor-element.e-con-full.e-flex.e-con.e-child"
        )
        items = driver.find_elements(
            By.CSS_SELECTOR, "a.elementor-element.e-con-full.e-flex.e-con.e-child"
        )
        for item in items:
            link = item.get_attribute("href").strip()
            title = driver.execute_script(
                "return arguments[0].innerText;",
                item.find_element(
                    By.CSS_SELECTOR, ".elementor-heading-title.elementor-size-default"
                ),
            )
            location = driver.execute_script(
                "return arguments[0].innerText;",
                item.find_elements(
                    By.CSS_SELECTOR, "p.elementor-heading-title.elementor-size-default"
                )[-1],
            )
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
