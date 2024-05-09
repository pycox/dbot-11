from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 339
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button#onetrust-reject-all-handler').click()
    except:
        print("No Cookie Button")

    time.sleep(2)

    data = []
    
    flag = True
    while flag:
        try:
            driver.execute_script("arguments[0].scrollIntoView(); window.scrollBy(0, -100);", driver.find_element(By.CSS_SELECTOR, "a.block-job-search__results-load"))
            driver.find_element(By.CSS_SELECTOR, "a.block-job-search__results-load").click()
            time.sleep(4)
        except Exception:
            flag = False
            print("No more page")
    
    items = driver.find_elements(By.CSS_SELECTOR, "li.block-job-search__result")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, ".block-job-search__result-location div").text.strip()
        if location in ["Birmingham", "Buckinghamshire", "London", "Newcastle upon Tyne", "Oxfordshire", "West Midlands", "Wiltshire", "Yorkshire", "Salisbury", "Bristol", "Glasgow", "East Sussex"]:
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, ".block-job-search__result-title").text.strip(),
                    com,
                    f"{location}, UK",
                    link,
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
