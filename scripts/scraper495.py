from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
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
        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Accept All"]').click()
    except:
        print("No Cookie Button")

    data = []
    
    if "UK" in locations:
        
        page = 1
        items = True

        while items:
            driver.get(f"{url}?page={page}")
            time.sleep(3)

            items = driver.find_elements(By.CSS_SELECTOR, "#search-result .border-slate-1")
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a[aria-label=\"Job detail page\"]").get_attribute("href").strip()
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "p.tt-jobName").text.strip(),
                        com,
                        "UK",
                        link,
                    ]
                )

            page += 1

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
