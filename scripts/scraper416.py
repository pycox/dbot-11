from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time
from bs4 import BeautifulSoup


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
        driver.get(
            "https://www.linkedin.com/jobs/channel-bakers-jobs-worldwide?f_C=6623499&trk=job-results_see-all-jobs-link&position=1&pageNum=0"
        )

        time.sleep(4)

        data = []

        driver.find_element(By.CSS_SELECTOR, "ul.jobs-search__results-list > li")

        soup = BeautifulSoup(driver.page_source, "html.parser")

        items = soup.select("ul.jobs-search__results-list > li")

        for item in items:
            link = item.select_one("a").get("href").strip()
            location = item.select_one(".job-search-card__location").text.strip()

            data.append(
                [
                    item.select_one("h3.base-search-card__title").text.strip(),
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
