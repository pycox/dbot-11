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

    time.sleep(3)

    try:
        driver.find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler').click()
    except:
        print("No Cookie Button")

    data = []

    for location in ["US", "GB"]:
        if location not in locations:
           continue

        driver.get(f"{url}?country={location}")
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
        items = driver.find_elements(By.CSS_SELECTOR, ".career-job-results-container .single .card .card-inner")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                    com,
                    location,
                    link,
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
