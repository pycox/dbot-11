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

    flag = True
    data = []

    time.sleep(4)
    try:
        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Yes, I agree"]').click()
    except:
        print("No Cookie Button")

    while flag:
        time.sleep(4)
        items = driver.find_elements(By.CSS_SELECTOR, ".wpb_column.vc_column_container.our_jobs_item")
        for item in items:
            link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            location = item.find_element(By.CSS_SELECTOR, '.joblocation').text.strip()
            for str in locations:
                if (str in location):
                    data.append(
                        [
                            item.find_element(By.CSS_SELECTOR, "h2").text.strip(),
                            com,
                            location,
                            link,
                        ]
                    )
                    break

        try:
          driver.find_element(By.CSS_SELECTOR, "main#main a.next.page-numbers > span").click()
          time.sleep(4)
        except:
          flag = False
          print("No More Jobs")


    driver.quit()

    updateDB(key, data)


if __name__ == "__main__":
    main()
