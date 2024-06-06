from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 511
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(2)

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".cmp-teaser.card")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                    com,
                    "United Kingdom",
                    link,
                ]
            )

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '.cmp-pagination__link-next')
            if "disabled" in next_button.get_attribute("class"):
                flag = False
            else:
                driver.execute_script("arguments[0].click();", next_button)
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
