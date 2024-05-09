from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 340
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".ListGridContainer .rowContainerHolder")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".rowItemsInnerContainer2 span:nth-child(1)").text.strip()
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
                    item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                    com,
                    location,
                    link,
                ]
            )

        try:
            driver.find_element(By.CSS_SELECTOR, 'a.normalanchor.ajaxable.scroller.scroller_movenext.buttonEnabled').click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
