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
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    data = []
    flag = True

    while flag:
        try:
            time.sleep(4)

            driver.find_element(
                By.CSS_SELECTOR, 'button[data-ui="load-more-button"]'
            ).click()

        except Exception as e:
            flag = False
            break

    items = driver.find_elements(By.CSS_SELECTOR, 'li[data-ui="job"]')

    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        title = item.find_element(By.CSS_SELECTOR, "h3").text.strip()
        location = item.find_element(By.CSS_SELECTOR, 'div[data-ui="job-location"]').text.strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        title,
                        com,
                        location,
                        link,
                    ]
                )
                break

    driver.quit()
    
    updateDB(key, data)


if __name__ == "__main__":
    main()
