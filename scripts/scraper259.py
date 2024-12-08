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

    data = []

    if "UK" in locations:
        flag = True
        while flag:
            time.sleep(4)
            items = driver.find_elements(By.CSS_SELECTOR, "section.apply-details__container")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )
            
            try:
                button = driver.find_element(By.CSS_SELECTOR, 'a.button.next')
                driver.execute_script("arguments[0].click();", button)
            except:
                flag = False
                print("No more Jobs")

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
