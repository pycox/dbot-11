from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import updateDB, eventHander
import time


def main(key, com, url):
    options = Options()
    
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    try:
        driver.find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(4)

    data = []
    
    if "UK" in locations:
        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "#searchResult-parent .row.p-3")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "button.btn-search-results-view").get_attribute("data-param1").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".ats-heading-font").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            try:
                curr_button = int(driver.find_element(By.CSS_SELECTOR, 'ul.pagination li.active a').text.strip())
                next_button = driver.find_element(By.CSS_SELECTOR, f'ul.pagination li a[data-pageno="{curr_button+1}"]')
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(4)
            except Exception:
                flag = False
                print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
