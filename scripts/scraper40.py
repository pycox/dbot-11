from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []

    items = driver.find_elements(By.CSS_SELECTOR, "a.elementor-element.e-con-full.e-flex.e-con.e-child")
    for item in items:
        link = item.get_attribute("href").strip()
        title = driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, ".elementor-heading-title.elementor-size-default"))
        location = driver.execute_script("return arguments[0].innerText;", item.find_elements(By.CSS_SELECTOR, "p.elementor-heading-title.elementor-size-default")[-1])
        for str in locations:
            if str in location:
                data.append(
                    [
                        title,
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
