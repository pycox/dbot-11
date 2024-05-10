from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main():
    key = 414
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)

    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, "section#open-positions div.ptcom-design__ctaWrap__xnniqk > a"))

    time.sleep(4)

    data = []

    items = driver.find_elements(By.CSS_SELECTOR, "section#open-positions li.ptcom-design__listItem__1pha1h")
    for item in items:
        title = item.find_element(By.CSS_SELECTOR, 'button').text.split("→")[0].strip()
        sub_items = item.find_elements(By.CSS_SELECTOR, "ul li a")
        driver.execute_script("arguments[0].classList.add('ptcom-design__sublistActive__1pha1h');", item.find_element(By.CSS_SELECTOR, "ul"))
        time.sleep(1)
        
        for sub_item in sub_items:
            link = sub_item.get_attribute("href").strip()
            location = sub_item.find_element(By.CSS_SELECTOR, 'span:nth-child(2)').text.strip()
            for str in ['D.C.', 'WA', 'NY', 'CA', 'London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
                if (str in location):
                    data.append(
                        [
                            title,
                            com,
                            location,
                            link,
                        ]
                    )
                    break

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
