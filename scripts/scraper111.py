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

    time.sleep(2)

    try:
        driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    data = []
    
    if "UK" in locations:
        
        flag = True
        while flag:
            time.sleep(4)
            try:
                driver.find_element(By.CSS_SELECTOR, "#js-careers-all > div > div > div > section > div.flex.flex-col.gap-8 > div > div > div > div > div.flex.justify-center.mt-10.sm\:flex-row.lg\:shrink-0.lg\:gap-4 > button").click()
            except Exception:
                flag = False
        
        items = driver.find_elements(By.CSS_SELECTOR, "article.js--careers-card")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            data.append(
                [
                    item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                    com,
                    "UK",
                    link,
                ]
            )


    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
