from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import readUrl, updateDB
import time


def main():
    key = 410
    com, url = readUrl(key)
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    if url.endswith("/"):
        url = url[:-1]
    driver.get(url)

    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, "#careers_recentJobPosts"))
    time.sleep(4)

    data = []
    
    flag = True
    while flag:
        time.sleep(4)
        try:
            driver.find_element(By.CSS_SELECTOR, "div#careers_recentJobPosts button").click()
        except Exception:
            flag = False
    
    items = driver.find_elements(By.CSS_SELECTOR, "div#careers_recentJobPosts a")
    for item in items:
        link = item.get_attribute("href").strip()
        location = "London"
        data.append(
            [
                item.find_element(By.CSS_SELECTOR, "p.heading-4").text.strip(),
                com,
                location,
                link,
            ]
        )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
