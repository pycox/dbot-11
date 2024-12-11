from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
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

    time.sleep(3)

    data = []
    
    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, ".vc_column-inner .wpb_wrapper .wpb_row.vc_row-fluid.vc_row.inner_row")
        for item in items[:-1]:
            item = item.find_element(By.XPATH, "./..") 
            link = item.find_element(By.CSS_SELECTOR, "a.nectar-button.large.regular.accent-color.regular-button").get_attribute("href").strip()
            data.append(    
                [
                    driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "h3")).strip(),
                    com,
                    "UK",
                    link,
                ]
            )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
