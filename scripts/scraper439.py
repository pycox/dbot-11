from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main():
    key = 439
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    flag = True
    data = []

    time.sleep(4)
    try:
        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Yes, I agree"]').click()
    except:
        print("No Cookie Button")

    while flag:
        time.sleep(4)
        items = driver.find_elements(By.CSS_SELECTOR, ".wpb_column.vc_column_container.our_jobs_item")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, '.joblocation').text.strip()
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
                    item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                    com,
                    location,
                    link,
                ]
            )

        try:
          driver.find_element(By.CSS_SELECTOR, "main#main a.next.page-numbers > span").click()
          time.sleep(4)
        except:
          flag = False
          print("No More Jobs")


    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
