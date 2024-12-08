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

    time.sleep(4)


    data = []
    flag = True

    while flag:
        items = driver.find_elements(By.CSS_SELECTOR, "div.content-block > ul > li[data-ph-at-id='jobs-list-item']")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, 'span.job-location').text.strip()
            location = location.replace("Location", "").replace("\n", "")

            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "div.job-title > span").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break
          
        try:
          driver.find_element(By.CSS_SELECTOR, "a[data-ph-at-id='pagination-next-link']").click()
          time.sleep(4)
        except:
          flag = False
          print("No More Pages")
              

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
