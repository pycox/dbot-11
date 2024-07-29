from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    flag = True
    while flag:
      try:
        driver.find_element(By.CSS_SELECTOR, "div.flex.justify-center > button").click()
        time.sleep(4)
      except:
        flag = False
        print("No more load button")


    data = []
    
    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, "div.comp-listing-vacancy_vacancy_item__RGJz4.vacancy-item")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "div.fs-title-4.text-greenDark.ss-sp-40").text.strip(),
                    com,
                    "UK",
                    link,
                ]
            )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
