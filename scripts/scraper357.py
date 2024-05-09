from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 357
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, '#cookiescript_close').click()
    except:
        print("No Cookie Button")

    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".attrax-list-widget__list--has-items .attrax-vacancy-tile")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".attrax-vacancy-tile__option-location-valueset p").text.strip()
            for location in ['Hammersmith', 'Knightsbridge', 'Thatcham', 'Harrods Estates', 'Heathrow - T1 London', 'Lakeside', 'City Road', 'Milton Keynes', 'Edinburgh', 'Bristol', 'Remote', 'Newcastle']:
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                        com,
                        f"{location}, UK",
                        link,
                    ]
                )

        try:
            driver.find_element(By.CSS_SELECTOR, 'main#main-site-main-content div.row.dragElement.widget.container-widget.wrapper-widget.job-results__pagination-container > div > div > div.attrax-pagination__pagination > ul > li.attrax-pagination__next > a').click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
