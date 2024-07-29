from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)

    data = []

    regions = {}
    locations = ["UK", "US"]

    if "UK" in locations:
        regions["GB"] = "United Kingdom"

    if "US" in locations:
        regions["US"] = "United States"


    for region_code, region in regions.items():
        url_ = f"{url}?optionsFacetsDD_country={region_code}"
        driver.get(url_)
        time.sleep(4)

        total_jobs = driver.find_element(By.CSS_SELECTOR, 'span.paginationLabel').text.strip()
        total_jobs = int(total_jobs.split("of")[1].strip())

        current_jobs = 0
        while current_jobs < total_jobs:
            items = driver.find_elements(By.CSS_SELECTOR, "tr.data-row")

            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                        com,
                        region,
                        link,
                    ]
                )

            current_jobs += 25
            if current_jobs < total_jobs:
                driver.get(url_ + f"&startrow={current_jobs}")
                time.sleep(4)

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
