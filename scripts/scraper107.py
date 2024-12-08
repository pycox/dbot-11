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

    try:
        driver.find_element(
            By.CSS_SELECTOR, "button.osano-cm-button--type_accept"
        ).click()
    except Exception as e:
        print(f"Scraper{key} cookiee button: {e}")

    time.sleep(4)

    flag = True
    data = []

    while flag:
        try:
            time.sleep(4)

            items = driver.find_elements(
                By.CSS_SELECTOR, "a.JobListings_listing__qqquK"
            )

            for item in items:
                link = item.get_attribute("href").strip()
                location = item.find_element(
                    By.CSS_SELECTOR, 'h4[data-testid="JobListings-location"]'
                ).text.strip()

                for str in locations:
                    if (str in location):
                        data.append(
                            [
                                item.find_element(
                                    By.CSS_SELECTOR, 'h3[data-testid="JobListings-title"]'
                                ).text.strip(),
                                com,
                                location,
                                link,
                            ]
                        )
                        break

            nextBtn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="next"]')

            if nextBtn.is_enabled():
                nextBtn.click()
            else:
                flag = False
        except:
            flag = False

    updateDB(key, data)


if __name__ == "__main__":
    main()
