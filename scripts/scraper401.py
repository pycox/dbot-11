from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
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
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    data = []
    
    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, "body > div.content-area > div:nth-child(3) > div.wp-block-group.gradient-dbl-tl.gradient-bl.has-space-900-background-color.has-background.is-layout-flow.wp-block-group-is-layout-flow > div.wp-block-custom > div")
        for item in items:
            data.append(
                [
                    driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "h3")).strip(),
                    com,
                    "UK",
                    item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip(),
                ]
            )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
