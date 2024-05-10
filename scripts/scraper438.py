from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main():
    key = 438
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    flag = True
    data = []

    time.sleep(4)
    try:
        driver.find_element(By.CSS_SELECTOR, 'button#CybotCookiebotDialogBodyButtonDecline').click()
    except:
        print("No Cookie Button")

    while flag:
        time.sleep(4)
        items = driver.find_elements(By.CSS_SELECTOR, ".careers-featured-cards")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, '.career-featured-card-location').text.strip()
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
                    item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                    com,
                    location,
                    link,
                ]
            )

        try:
          driver.find_element(By.CSS_SELECTOR, "a.px-4.py-2.border.bg-white.leading-2").click()
          time.sleep(4)
        except:
          flag = False
          print("No More Jobs")


    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
