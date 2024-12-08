from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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


    data = []

    if "UK" in locations:
    
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "div.jobs-card")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                curr_button = int(driver.find_element(By.CSS_SELECTOR, 'li.active a.page-update').text.strip())
                next_button = driver.find_element(By.CSS_SELECTOR, f'li a[data-page="{curr_button+1}"]')
                driver.execute_script("arguments[0].click();", next_button)
                
                time.sleep(6)
            except Exception as e:
                flag = False
                print("No More Jobs", e)
            

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
