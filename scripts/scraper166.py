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

    flag = True
    data = []

    time.sleep(4)

    try:
        driver.find_element(
            By.CSS_SELECTOR, "button#didomi-notice-agree-button"
        ).click()
    except Exception as e:
        print(f"Scraper{key} cookiee button: {e}")
        
    while flag:
        try:
            time.sleep(4)

            items = driver.find_elements(By.CSS_SELECTOR, "li.ts-offer-list-item")

            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                location = item.find_element(
                    By.CSS_SELECTOR, "li.noBorder"
                ).text.strip()

                for str in locations:
                    if str in location:

                        data.append(
                            [
                                item.find_element(
                                    By.CSS_SELECTOR, "h3.ts-offer-list-item__title"
                                ).text.strip(),
                                com,
                                location,
                                link,
                            ]
                        )

                        break

            nextBtn = driver.find_elements(
                By.CSS_SELECTOR, "a.ts-ol-pagination-list-item__link--next"
            )

            if len(nextBtn) > 0:

                nextBtn[0].click()
            else:
                flag = False
                break
        except:
            flag = False

    driver.quit()
    
    print(data)
    return

    updateDB(key, data)


if __name__ == "__main__":
    main()
