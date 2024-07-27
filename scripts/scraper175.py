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

    time.sleep(8)


    items = driver.find_elements(By.CSS_SELECTOR, "#open-positions ul li ul li ul li")

    data = []

    for item in items:
        button = item.find_elements(By.CSS_SELECTOR, "button")
        if not button:
            continue
        button = button[0]
        driver.execute_script("arguments[0].click();", button)
        title = item.find_element(By.CSS_SELECTOR, "button").text.split("\n")[0].strip()
        locs = item.find_elements(By.CSS_SELECTOR, 'a')
        for location in locs:
            link = location.get_attribute("href").strip()
            location = driver.execute_script("return arguments[0].innerText;", location).replace("↳", "").strip()
            for str in locations:
                if (str in location):
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
