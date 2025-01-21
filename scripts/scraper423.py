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
            driver.find_element(By.CSS_SELECTOR, "#igdpr-reject-button").click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        data = []

        regions = []

        regions.append(
            (
                "United Kingdom",
                "https://www.clubmedjobs.com/en/search-jobs?orgIds=2619&ascf=[{%22key%22:%22campaign%22,%22value%22:%22Office%22}]",
            )
        )

        regions.append(
            (
                "United States",
                "https://www.clubmedjobs.com/en/search-jobs/United%20States?orgIds=2619&alp=6252001&alt=2&ascf=[{%22key%22:%22campaign%22,%22value%22:%22Resort%22}]",
            )
        )

        driver.find_element(By.CSS_SELECTOR, "ul.job-list li.job-list__item")

        for location, uri in regions:
            driver.get(uri)

            flag = True

            while flag:
                items = driver.find_elements(
                    By.CSS_SELECTOR, "ul.job-list li.job-list__item"
                )

                for item in items:
                    link = (
                        item.find_element(By.CSS_SELECTOR, "a")
                        .get_attribute("href")
                        .strip()
                    )

                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )

                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
                    driver.execute_script("arguments[0].scrollIntoView();", next_button)
                    time.sleep(2)
                    if "disabled" in next_button.get_attribute("class"):
                        flag = False
                    else:
                        next_button.click()
                    time.sleep(4)
                except Exception:
                    flag = False

            try:
                button = driver.find_element(
                    By.CSS_SELECTOR, f'input[data-display="{location}"]'
                )
                driver.execute_script("arguments[0].scrollIntoView();", button)
                driver.execute_script("arguments[0].click();", button)
                time.sleep(5)
            except Exception:
                continue

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
