from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 498
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    for location, loc_code in [("USA", "204"), ("London", "174")]:
        Select(driver.find_element(By.CSS_SELECTOR, "select#field_31")).select_by_value(loc_code)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "#submit").click()
        time.sleep(4)

        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".vacancy")
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

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, '.paging_links a:nth-child(1)')
                if not next_button.text.startswith("Next"):
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
