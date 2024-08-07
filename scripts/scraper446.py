from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(6)

    data = []
    
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, "#icims_content_iframe"))
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "icims_content_iframe")))
    driver.switch_to.frame(iframe)
    time.sleep(6)
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".iCIMS_JobsTable .row")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_elements(By.CSS_SELECTOR, "span")[1].text.strip()
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break
        
        try:
            button = driver.find_element(By.CSS_SELECTOR, 'a:not(.invisible) span[title="Next page of results"')
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
