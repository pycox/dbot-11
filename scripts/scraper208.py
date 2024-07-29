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

    flag = True
    while flag:

        items = driver.find_elements(By.CSS_SELECTOR, "article.article.article--result")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, ".article__header__actions a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, 'div.article__header__text__subtitle > span:last-child').text.strip()

            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "h3 a").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break

                
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a.paginationNextLink')
            next_button.click()
            time.sleep(4)
        except:
            flag = False
            print("No More Jobs")

    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
