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
        driver.find_element(By.CSS_SELECTOR, '.cookieinfo-close').click()
    except:
        print("No Cookie Button")
    
    time.sleep(2)
    data = []
    
    if "UK" in locations:
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".rgMasterTable tbody tr.rgRow")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                button = driver.find_element(By.CSS_SELECTOR, 'button[title="Next Page"]')
                if button.get_attribute("onclick").startswith("return"):
                    flag = False
                else:
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
