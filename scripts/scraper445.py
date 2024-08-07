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
        driver.find_element(By.CSS_SELECTOR, '#cookie-accept').click()
    except:
        print("No Cookie Button")

    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, "#searchresults tbody tr")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, ".jobLocation")).strip()
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

        try:
            curr_button = int(driver.find_element(By.CSS_SELECTOR, '.pagination li.active a').text.strip())
            next_button = driver.find_element(By.CSS_SELECTOR, f'.pagination li a[title="Page {curr_button+1}"]')
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
