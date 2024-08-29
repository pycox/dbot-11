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

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".css-ldt7kr")
    for item in items:
        try:
            title = item.find_element(By.CSS_SELECTOR, "a").text.strip()
            if len(title.split("-")) == 2:
                title, location = title.split("-")
                title, location =  title.strip(), location.strip()
            else:
                location = item.find_element(By.CSS_SELECTOR, ".jss-f77").text.strip()
        except:
            continue
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
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
