from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
    if all(loc in locations for loc in ["US", "UK"]):
        url += "?locationCountry=bc33aa3152ec42d4995f4791a106ed09&locationCountry=29247e57dbaf46fb855b224e03170bc7"
    elif "US" in locations:
        url += "?locationCountry=bc33aa3152ec42d4995f4791a106ed09"
    elif "UK" in locations:
        url += "?locationCountry=29247e57dbaf46fb855b224e03170bc7"

    driver.get(url)
    flag = True
    data = []

    while flag:
        try:
            time.sleep(4)

            items = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")

            for item in items:
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                location = item.find_element(By.CSS_SELECTOR, "dd").text.strip()

                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "a").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )

            if (
                len(
                    driver.find_elements(
                        By.CSS_SELECTOR, "button[data-uxi-element-id='next']"
                    )
                )
                > 0
            ):
                driver.find_element(
                    By.CSS_SELECTOR, "button[data-uxi-element-id='next']"
                ).click()
            else:
                flag = False
                break

        except Exception as e:
            flag = False

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
