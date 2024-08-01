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

    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, "#search > div > div > ul > li")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, "div[data-test-component=\"StencilText\"]").text.strip()
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next page"]')
            if "true" == next_button.get_attribute("aria-disabled"):
                flag = False
            else:
                next_button.click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
