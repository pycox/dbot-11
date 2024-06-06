from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import readUrl, updateDB
import time


def main():
    key = 528
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(4)

    data = []

    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "jv_careersite_iframe_id")))
    driver.switch_to.frame(iframe)
    items = driver.find_elements(By.CSS_SELECTOR, ".jv-featured-job")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
        location = " ".join(item.find_element(By.CSS_SELECTOR, ".jv-featured-job-location").text.strip().split(" ")[1:])
        for str in ['London', 'New York', 'San Francisco', 'United States', 'United Kingdom', 'UK', 'USA', 'US']:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, ".jv-featured-job-title").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )


    driver.quit()
    print(key, data)


if __name__ == "__main__":
    main()
