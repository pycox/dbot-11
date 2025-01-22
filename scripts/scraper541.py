from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import updateDB, eventHander
import time
from selenium_stealth import stealth


def main(key, com, url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36"

    options = webdriver.ChromeOptions()

    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent={}".format(user_agent))
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    try:
        driver.get(url)

        time.sleep(8)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(4)

        data = []

        flag = True

        driver.find_element(By.CSS_SELECTOR, "div.vsr-job-big")

        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "div.vsr-job-big")

            for item in items:
                link = (
                    item.find_element(By.CSS_SELECTOR, "a")
                    .get_attribute("href")
                    .strip()
                )

                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                curr_button = int(
                    driver.find_element(
                        By.CSS_SELECTOR, '.paginator span[aria-current="true"]'
                    ).text.strip()
                )
                next_button = driver.find_element(
                    By.CSS_SELECTOR, f'.paginator a[title="Go to page {curr_button+1}"]'
                )
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                driver.execute_script("arguments[0].click();", next_button)
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
