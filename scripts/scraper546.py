from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
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
