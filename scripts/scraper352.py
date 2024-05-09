from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 352
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".col-xs-12.col-sm-6.col-md-3")
        print(items)
        for item in items:
            print(item)
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".value_location").text.strip()
            for str in [
                "Belfast", "Birmingham", "Bournemouth", "Bristol", "Channel Islands", "Cheltenham", "Edinburgh",
                "Exeter", "Glasgow", "Guernsey", "Jersey", "Leeds", "Liverpool", "Manchester", "Reading", "Reigate",
                "Sheffield", 'London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US'
            ]:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "strong").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.next')
            if "disabled" in next_button.get_attribute("class"):
                flag = False
            else:
                next_button.click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
