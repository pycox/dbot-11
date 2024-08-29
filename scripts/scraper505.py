from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button[show.bind="showDeclineButton"]').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, "li.jobs-list-item")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            try:
                location = item.find_element(By.CSS_SELECTOR, ".job-location").text.split("\n")[-1].strip()
            except:
                continue
            print(location)
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, ".job-title").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break

        try:
            button = driver.find_element(By.CSS_SELECTOR, 'a:not(.aurelia-hide)[aria-label="View next page"]')
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
