from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "frame[title=\"Site content frame\"]")))
    driver.switch_to.frame(iframe)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(4)

    flag = True
    while flag:
        time.sleep(4)
        try:
            button = driver.find_element(By.CSS_SELECTOR, "button.Mhr-jobSearchMoreResultsButton")
            driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()
        except Exception as e:
            print(e)
            flag = False


    data = []

    
    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, ".Mhr-jobSearchJobs .Mhr-jobDetail")
        for item in items:
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "a span").text.strip(),
                    com,
                    "UK",
                    url,
                ]
            )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
