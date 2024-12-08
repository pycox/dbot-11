from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import updateDB, eventHander
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    try:
        driver.find_element(By.CSS_SELECTOR, '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll').click()
    except:
        print("No Cookie Button")
    time.sleep(4)

    data = []
    
    total_count = int(driver.find_element(By.CSS_SELECTOR, ".pagination__count span:nth-child(2)").text.strip())
    while total_count > 0:
        items = driver.find_elements(By.CSS_SELECTOR, ".table.careers-vacancies-listing__table tr")
        for item in items[1:]:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, "td:nth-child(3) p:nth-child(2)").text.strip()
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break
        
        try:
            total_count -= 15
            if total_count > 15:
                button = driver.find_element(By.CSS_SELECTOR, 'button[title="next"]')
                driver.execute_script("arguments[0].click();", button)
                time.sleep(4)
        except:
            total_count = 0
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
