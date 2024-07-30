from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    
    try:
        driver.find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler').click()
    except:
        print("No Cookie Button")

    data = []
    
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
    driver.switch_to.frame(iframe)

    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, "table.jobListPanel > tbody > tr")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, 'td:last-child').text.strip()
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
            links = driver.find_elements(By.CSS_SELECTOR, '.pagingPanel a')
            next_page = links[-2]
            if next_page.text.strip() == "Next":
                driver.execute_script("arguments[0].click();", next_page)
            else:
                flag = False
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
