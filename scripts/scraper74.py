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

    try:
        driver.find_element(By.CSS_SELECTOR,"#accept_all_cookies_button").click()
    except Exception as e:
        print(f"Scraper{key} cookiee button: {e}")

    time.sleep(4)

    driver.find_element(By.CSS_SELECTOR, "#submitSearch").click()
    time.sleep(4)
    
    data = []
    flag = True

    if "UK" in locations:
        while flag:
            items = driver.find_elements(By.CSS_SELECTOR, "li.search-results-job-box")

            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                        com,
                        "United Kingdom",
                        link,
                    ]
                )
            
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a[title="Go to next search results page"]')
                next_button.click()
                time.sleep(4)
            except:
                flag = False
                print("No More Jobs")
        

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
