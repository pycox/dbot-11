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
        driver.find_element(By.CSS_SELECTOR, "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
    except:
        print("No Cookie Button")

    time.sleep(4)
    
    data = []
    
    flag = True

    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".job-search .featured-jobs-item")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a.apply-link").get_attribute("href").strip()
            location = item.find_elements(By.CSS_SELECTOR, "span.job-info")[1].text.split(":")[-1].strip()
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, ".job-title").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break

        try:
            button = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
