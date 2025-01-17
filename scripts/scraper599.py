from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

    items = driver.find_elements(By.CSS_SELECTOR, "div.fab-CardContent.fab-CardContent--customSpacing > ul > div")

    data = []

    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "div > a").get_attribute("href").strip()
        location = item.find_elements(By.CSS_SELECTOR, 'p')[1].text.strip()
        
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

    driver.quit()

    updateDB(key, data)

if __name__ == "__main__":
    main()