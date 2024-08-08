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
    
    try:
        driver.find_element(By.CSS_SELECTOR, 'button[data-action="click->common--cookies--alert#disableAll"]').click()
    except:
        print("No Cookie Button")
    time.sleep(3)

    flag = True
    while flag:
      try:
        driver.find_element(By.CSS_SELECTOR, 'a#show_more_button').click()
        time.sleep(4)
      except:
        flag = False
        print("No more Jobs")

    items = driver.find_elements(By.CSS_SELECTOR, "ul#jobs_list_container > li")

    data = []

    if "UK" in locations:
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "span").text.strip(),
                    com,
                    "UK",
                    link,
                ]
            )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
