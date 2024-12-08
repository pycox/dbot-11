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
        driver.find_element(By.CSS_SELECTOR, 'button#hs-eu-decline-button').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    sub_links = []
    
    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, 'ul[data-rte-list="default"] li p a:nth-child(1)')
        for item in items:
            link = item.get_attribute("href").strip()
            if link.startswith("https://phf.tbe.taleo.net"):
                sub_links.append(link)
            else:
                data.append(
                    [
                        item.text.strip(),
                        com,
                        "US",
                        link,
                    ]
                )

        for link in sub_links:
            driver.get(link)
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, 'button.fa-search').click()
            time.sleep(4)
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                
                
            items = driver.find_elements(By.CSS_SELECTOR, 'h4.oracletaleocwsv2-head-title')
            for item in items:
                link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute("href").strip()
                data.append(
                    [
                        item.text.strip(),
                        com,
                        "US",
                        link,
                    ]
                )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
