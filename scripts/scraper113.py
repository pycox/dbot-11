from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(2)

    data = []
    regions = []

    if "UK" in locations:
        regions.append("United Kingdom")
    if "US" in locations:
        regions.append("United States")
    
    button = driver.find_element(By.CSS_SELECTOR, "#search-filter-clear")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)
    
    button = driver.find_element(By.CSS_SELECTOR, "#country-toggle")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)

    for region in regions:
        button = driver.find_element(By.CSS_SELECTOR, f'input[data-display="{region}"]')
        driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(4)

    flag = True
    
    if regions:
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "#search-results-list li a")
            for item in items:
                link = item.get_attribute("href").strip()
                title = driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "h3"))
                
                data.append(
                    [
                        title.strip(),
                        com,
                        driver.execute_script("return arguments[0].innerText;", item.find_element(By.CSS_SELECTOR, "span.job-location")),
                        link,
                    ]
                )

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')
                if "disable" in next_button.get_attribute("class"):
                    flag = False
                else:
                    driver.execute_script("arguments[0].click();", next_button)
                    
                time.sleep(4)
            except Exception as e:
                flag = False
                print("No More Jobs", e)
    
    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
