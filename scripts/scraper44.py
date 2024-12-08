from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
from bs4 import BeautifulSoup
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
            driver.find_element(By.CSS_SELECTOR, "button#cookie-accept").click()
        except Exception as e:
            print(f"{key} ==== cookiee button ====: {e}")
            eventHander(key, "ELEMENT")

        time.sleep(4)

        data = []
        flag = True

        while flag:
            try:
                time.sleep(4)

                driver.find_element(By.CSS_SELECTOR, "button#tile-more-results").click()

            except Exception as e:
                flag = False
                break

        driver.find_element(By.CSS_SELECTOR, "li.job-tile")

        soup = BeautifulSoup(driver.page_source)

        items = soup.select("li.job-tile")

        for item in items:
            link_tag = item.select_one("a")
            link = link_tag["href"].strip() if link_tag else None

            title_tag = item.select_one("span.section-title")
            title = title_tag.text.strip() if title_tag else None

            location_tag = item.find(
                lambda tag: tag.name == "span" and "Location" in tag.text
            )
            location = (
                location_tag.find_next_sibling("div").text.strip()
                if location_tag
                else None
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
