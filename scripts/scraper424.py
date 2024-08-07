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

    data = []
    regions = []
    
    if "UK" in locations:
        regions.append(("UK", "5575"))
    
    if "US" in locations:
        regions.append(("US", "5570"))
    
    for location, location_code in regions:
        driver.get(f"{url}&groupType_114={location_code}")
        time.sleep(4)

        flag = True
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, ".cvmJobBoardHeader tr.odd, .cvmJobBoardHeader tr.even")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".jbTableTextStyle").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            try:
                button = driver.find_element(By.CSS_SELECTOR, 'input[name="next_page"]')
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
