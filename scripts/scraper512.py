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
        driver.find_element(By.CSS_SELECTOR, '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(4)

    data = []
    
    if "UK" in locations:
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "#JobFilterResults .job-summary")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                curr_button = int(driver.find_element(By.CSS_SELECTOR, 'nav[aria-label="Pagination"] li.page.active').text.strip())
                next_button = driver.find_element(By.CSS_SELECTOR, f'nav[aria-label="Pagination"] li.page a[aria-label="Go to page {curr_button+1}"]')
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
