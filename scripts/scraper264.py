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

    flag = True
    while flag:
        try:
            button = driver.find_element(By.CSS_SELECTOR, "#roles-archive > div.min-h-\[300px\] > div > div > div:nth-child(2) > div.mt-10.flex.justify-center.sm\:mt-20 > button")
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(4)
        except Exception:
            flag = False
            print("No more Load Button")

    time.sleep(4)
    items = driver.find_elements(By.CSS_SELECTOR, "div.grid.grid-cols-1.gap-6 > a")

    data = []
    for item in items:
        link = item.get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, 'span.body-small.body-bold.text-grey-secondary').text.strip()

        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
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
