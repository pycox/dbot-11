from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 351
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler").click()
    except:
        print("No Cookie Button")

    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".attrax-list-widget__list.attrax-list-widget__list--list.attrax-list-widget__list--has-items .attrax-vacancy-tile")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a[aria-label='Apply now']").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".attrax-vacancy-tile__option-location-valueset").text.strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "a.attrax-vacancy-tile__title").text.strip(),
                    com,
                    f"{location}, United Kingdom",
                    link,
                ]
            )

        try:
            driver.find_element(By.CSS_SELECTOR, 'main#main-site-main-content div.cop-widget.dynamic-widget.attrax-list-pagination-widget.job-results__top-pagination.list-data-pagination-widget > div.attrax-pagination__pagination > ul > li.attrax-pagination__next > a').click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
