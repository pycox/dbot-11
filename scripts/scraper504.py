from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 504
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, ".seo-pages-100b19y-StyledLocationAndJobs.e2oznfq0")
    for item in items:
        location = item.find_element(By.CSS_SELECTOR, ".seo-pages-1va6nd7-StyledText").text.strip()
        for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US', 'CA', 'WA', 'TX']:
            if (str in location):
                subitems = driver.find_elements(By.CSS_SELECTOR, ".seo-pages-1cxckch-StyledUrlWrapper.epip1yb0")
                for subitem in subitems:
                    data.append(
                        [
                            subitem.find_element(By.CSS_SELECTOR, "a").text.strip(),
                            com,
                            location,
                            subitem.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip(),
                        ]
                    )
                break


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
