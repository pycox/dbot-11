from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main():
    key = 505
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)
    
    try:
        driver.find_element(By.CSS_SELECTOR, 'button.cc-nb-okagree').click()
        time.sleep(4)
    except:
        print("No Cookiee") 
        
    data = []
    
    flag = True
    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, ".job-search-section__result a.job-card")
        for item in items:
            link = item.get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, ".job-card__list li:nth-child(1)").text.strip()
            for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
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
            next_button = driver.find_element(By.CSS_SELECTOR, '.pagination__btn--next')
            if "is-disabled" in next_button.get_attribute("class"):
                flag = False
            else:
                driver.execute_script("arguments[0].click();", next_button)
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
