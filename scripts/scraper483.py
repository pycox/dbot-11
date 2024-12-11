from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import updateDB, eventHander
import time


def main(key, com, url):
    options = Options()
    
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button#hs-eu-decline-button').click()
        driver.find_element(By.CSS_SELECTOR, 'button[data-automation-id="legalNoticeDeclineButton"]').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(4)

    data = []
    
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "personio-iframe")))
    driver.switch_to.frame(iframe)
    
    items = driver.find_elements(By.CSS_SELECTOR, "a.job-box-link.job-box")
    for item in items:
        link = item.get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, ".multi-offices-desktop")
        location = driver.execute_script("return arguments[0].innerText;", location).split("·")[-1].strip()
        for str in locations:
            if (str in location):
                data.append(
                    [
                        driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, ".jb-title")).strip(),
                        com,
                        location,
                        link,
                    ]
                )
                break


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
