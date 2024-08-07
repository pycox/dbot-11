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
        items = driver.find_elements(By.CSS_SELECTOR, ".applications-content a.applications-row")
        for item in items:
            link = item.get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".applications-where").text.strip()
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

        try:
            button = driver.find_elements(By.CSS_SELECTOR, '.pager-row tr td')[-2].find_element(By.CSS_SELECTOR, 'a')
            if button.text.strip() == "Next":
                button.click()
            else:
                flag = False
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
