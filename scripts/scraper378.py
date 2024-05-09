from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 378
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'a#hs-eu-confirmation-button').click()
    except:
        print("No Cookie Button")

    data = []
    
    flag = True
    while flag:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, ".pagination"))
        time.sleep(4)
        items = driver.find_elements(By.CSS_SELECTOR, "article.single-job-opportunity")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".single-job-opportunity__result").text.strip()
            if location in ["New York"]:
                location = f"{location}, US"
            elif location in [
                "Belfast", "Birmingham", "Bournemouth", "Bristol", "Channel Islands", "Cheltenham", "Edinburgh",
                "Exeter", "Glasgow", "Guernsey", "Jersey", "Leeds", "Liverpool", "Manchester", "Reading", "Reigate",
                "Sheffield", 
            ]:
                location = f"{location}, UK"
            elif any(substring in location for substring in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']):
                pass
            else:
                continue
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                    com,
                    location,
                    link,
                ]
            )

        try:

            driver.find_element(By.CSS_SELECTOR, 'a.next').click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
