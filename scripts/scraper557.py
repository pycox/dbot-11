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

    time.sleep(3)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    
    items = driver.find_elements(By.CSS_SELECTOR, "ul.job-list li")
    for item in items:
        link = f'{url}?jobId={item.get_attribute("data-jobid").strip()}'
        data.append(
            [
                item.find_element(By.CSS_SELECTOR, ".job-title").text.strip(),
                com,
                "UK",
                link,
            ]
        )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
