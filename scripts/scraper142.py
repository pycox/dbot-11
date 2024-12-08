from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

    try:
        driver.find_element(By.CSS_SELECTOR, "a.btn.aceptar").click()
    except Exception as e:
        print(f"Scraper{key} cookie Button: {e}")

    flag = True
    data = []

    while flag:
        try:
            time.sleep(4)

            items = driver.find_elements(By.CSS_SELECTOR, "li.careers__list__item")

            for item in items:
                location = item.find_element(
                    By.CSS_SELECTOR, "div.news-grid__items_publish_date"
                ).text.strip()
                title = item.find_element(
                    By.CSS_SELECTOR, "p.news-grid__items_title"
                ).text.strip()
                for str in locations:
                    if (str in location):
                        data.append(
                            [
                                title,
                                com,
                                location,
                                url,
                            ]
                        )
                        break
            try:
                nextBtn = driver.find_element(By.CSS_SELECTOR, "a.next.page-numbers")
                nextBtn.click()
            except:
                flag = False
        except:
            flag = False

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
