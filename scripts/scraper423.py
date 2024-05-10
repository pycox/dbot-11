from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import readUrl, updateDB
import time


def main():
    key = 423
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler').click()
    except:
        print("No Cookie Button")
        
    data = []
    
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
    driver.switch_to.frame(iframe)
    time.sleep(4)
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".list.jobListPanel tbody tr")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            title = item.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
            location = item.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()
            for str in ['Chicago', 'London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
                if (str in location):
                    data.append(
                        [
                            title,
                            com,
                            location,
                            link,
                        ]
                    )
                    break

        try:
            next_button = driver.find_elements(By.CSS_SELECTOR, '.pagingPanel a')[0]
            if next_button.text.strip() == "Next":
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(4)
            else:
                flag = False
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
