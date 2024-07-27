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

    flag = True
    while flag:
        time.sleep(4)
        try:
            button = driver.find_element(By.CSS_SELECTOR, "#show_more_button")
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
        except Exception:
            flag = False

    items = driver.find_elements(By.CSS_SELECTOR, "ul#jobs_list_container > li")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        data.append(
            [
                driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "span")).strip(),
                com,
                "UK",
                link,
            ]
        )

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
