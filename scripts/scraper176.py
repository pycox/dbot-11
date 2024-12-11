from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".careers-page iframe")))
    driver.switch_to.frame(iframe)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, "#benefits"))

    time.sleep(4)

    data = []

    items = driver.find_elements(By.CSS_SELECTOR, ".open-pos--single-block")
    for item in items:
        title = item.find_element(By.CSS_SELECTOR, 'h1').text.strip()
        sub_items = item.find_elements(By.CSS_SELECTOR, "div[role='listitem'] a")
        for sub_item in sub_items:
            location = sub_item.find_element(By.CSS_SELECTOR, 'div').text.strip()
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            title,
                            com,
                            location,
                            sub_item.get_attribute("href").strip(),
                        ]
                    )
                    break

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
