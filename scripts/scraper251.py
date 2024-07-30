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
      select = Select(driver.find_element(By.CSS_SELECTOR, "div.perpage-select > select"))
      select.select_by_visible_text("100")
    except:
      print("No Select working")

    time.sleep(4)
    data = []


    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, "table.ats_list > tbody > tr")

        for item in items:
            link = item.get_attribute("onclick").strip().replace("window.location.href=", "").replace("'", "")
            link = "https://ryman.ats.emea1.fourth.com" + link
            
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "td:first-child").text.strip(),
                    com,
                    "UK",
                    link,
                ]
            )
            
        try:
            curr_button = int(driver.find_element(By.CSS_SELECTOR, 'li.page-item.active a').text.strip())
            next_button = driver.find_element(By.CSS_SELECTOR, f'li a[data-page="{curr_button+1}"]')
            next_button.click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")
    
    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
