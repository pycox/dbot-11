from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils import updateDB, eventHander
import time


def main(key, com, url):
    options = Options()
    
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(3)

    try:
        driver.find_element(By.CSS_SELECTOR, '.accept-cookies.js-accept-cookies').click()
    except:
        print("No Cookie Button")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    data = []
    
    if "UK" in locations:
        items = driver.find_elements(By.CSS_SELECTOR, "span.tab-heading.js-tab-heading")
        for item in items:
            driver.execute_script("arguments[0].click();", item)
            time.sleep(1)
            content_div = item.find_element(By.XPATH, "./following-sibling::div[@class='tab-content js-tab-content']")
            sub_items = content_div.find_elements(By.CSS_SELECTOR, ".tab-content.js-tab-content p a[rel=\"noopener noreferrer\"]")
            for sub_item in sub_items:
                link = sub_item.get_attribute("href").strip()
                title = link.replace(".pdf", "").split("/jd-")[-1].replace("-"," ").title()
                data.append(
                    [
                        title,
                        com,
                        "UK",
                        link,
                    ]
                )

    driver.quit()
    updateDB(key, data)


if __name__ == "__main__":
    main()
