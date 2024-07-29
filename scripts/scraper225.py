from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import readUrl, updateDB
import time


def main(key, com, url, locations):

    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(4)


    data = []

    items = driver.find_elements(By.CSS_SELECTOR, "div.v2_m_small.w-dyn-item")
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a.v2_text_link.w-condition-invisible").get_attribute("href").strip()
        location = item.find_element(By.CSS_SELECTOR, 'div.v2_card--content--subheading.v2_light_gray').text.strip()

        for str in locations:
            if (str in location):
                data.append(
                    [
                        item.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                        com,
                        location,
                        link,
                    ]
                )
                break

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
