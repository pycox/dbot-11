from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
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
