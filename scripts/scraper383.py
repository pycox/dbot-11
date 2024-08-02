from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    

    if "UK" in locations:
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[width=\"100%\"]")))
        driver.switch_to.frame(iframe)
        time.sleep(4)
        
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, "tbody"))
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
            
        
        items = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        for item in items:
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "td").text.strip(),
                    com,
                    "UK",
                    item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip(),
                ]
            )

        driver.quit()
        updateDB(key, data)


if __name__ == "__main__":
    main()
