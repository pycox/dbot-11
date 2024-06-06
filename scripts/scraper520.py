from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 520
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    
    data = []
        
    flag = True

    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                    com,
                    "USA",
                    link,
                ]
            )

        
        try:
            driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, 'button[data-uxi-element-id="next"]'))
            time.sleep(4)
        except Exception:
            flag = False
            print("No More Jobs")
    
    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
