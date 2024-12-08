from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import updateDB, eventHander
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(3)

    try:
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title=\"SP Consent Message\"]")
        driver.switch_to.frame(iframe)
        button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="I Agree"]')
        driver.execute_script("arguments[0].click();", button)
        driver.switch_to.default_content()
        time.sleep(2)
    except:
        print("No Cookie Button")


    data = []

    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, "div#ctl00_ctl00_ContentContainer_mainContent_ctl00_jobResultListNew > div.vsr-job")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, 'div[data-id="div_content_VacV_LocationID"] > span').text.strip()

            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                    com,
                    location,
                    link,
                ]
            )
        
        try:
            curr_button = int(driver.find_element(By.CSS_SELECTOR, '.paginator.paginator--bottom .cpb').text.strip())
            next_button = driver.find_element(By.CSS_SELECTOR, f'.paginator.paginator--bottom a[title="Go to page {curr_button+1}"]')
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
