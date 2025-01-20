from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
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
            select = Select(
                driver.find_element(By.CSS_SELECTOR, "div.perpage-select > select")
            )
            select.select_by_visible_text("100")
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        time.sleep(4)
        data = []

        flag = True

        driver.find_element(By.CSS_SELECTOR, "table.ats_list > tbody > tr")

        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "table.ats_list > tbody > tr")

            for item in items:
                link = (
                    item.get_attribute("onclick")
                    .strip()
                    .replace("window.location.href=", "")
                    .replace("'", "")
                )
                link = "https://ryman.ats.emea1.fourth.com" + link

                data.append(
                    [
                        item.find_element(
                            By.CSS_SELECTOR, "td:first-child"
                        ).text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                curr_button = int(
                    driver.find_element(
                        By.CSS_SELECTOR, "li.page-item.active a"
                    ).text.strip()
                )
                next_button = driver.find_element(
                    By.CSS_SELECTOR, f'li a[data-page="{curr_button+1}"]'
                )
                next_button.click()
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")

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
