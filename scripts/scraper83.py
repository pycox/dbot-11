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

        time.sleep(4)

        try:
            driver.find_element(By.CSS_SELECTOR, "button#cookie-acknowledge").click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        flag = True

        while flag:
            try:
                time.sleep(2)

                loadBtn = driver.find_element(
                    By.CSS_SELECTOR, "button#tile-more-results"
                )

                loadBtn.click()
            except Exception as e:
                flag = False

        dom = driver.find_element(By.CSS_SELECTOR, "ul#job-tile-list")

        dom.find_element(By.CSS_SELECTOR, "li")
        items = dom.find_elements(By.CSS_SELECTOR, "li")

        data = []

        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = (
                item.find_element(By.XPATH, ".//span[contains(text(), 'Location')]")
                .find_element(By.XPATH, "./following-sibling::div")
                .text.strip()
            )

            data.append(
                [
                    item.find_element(
                        By.CSS_SELECTOR, "span.section-title"
                    ).text.strip(),
                    com,
                    item.find_element(By.XPATH, ".//span[contains(text(), 'Location')]")
                    .find_element(By.XPATH, "./following-sibling::div")
                    .text.strip(),
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
