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

    try:
        driver.find_element(By.CSS_SELECTOR, 'button#accept-cookies').click()
    except:
        print("No Cookie Button")

    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".items-stretch.ng-star-inserted a.ng-star-inserted")
        for item in items:
            link = item.get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, "p.paragraph-2.font-medium.text-neutral-600").text.strip()
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
            
            next_button = driver.find_element(By.CSS_SELECTOR, '#next-page')
            if next_button.get_attribute("disabled"):
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
